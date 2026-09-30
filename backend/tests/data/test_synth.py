from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mantle_data import schemas as S
from mantle_data.synth import s1_roster, s2_cycles, s3_telemetry, s4_cards, s5_failures, s6_traces
from mantle_data.synth.common import SCALES, frame_hash, get_scale
from mantle_physics import DYNO_CLASSES, WellSim
from mantle_physics.hazard import rod_damage_rate


@pytest.fixture(scope="module")
def tables(built):
    syn = built["syn"]
    rd = lambda n: pd.read_parquet(syn / f"{n}.parquet")  # noqa: E731
    return {n: rd(n) for n in ("wells", "cycles", "cycle_daily", "failures", "unseats", "workovers",
                                "optimiser_traces", "telemetry_events")}


def test_scales_defined():
    assert set(SCALES) == {"small", "default", "enormous"}
    assert get_scale("default").n_wells == 60 and get_scale("enormous").n_wells == 400
    assert get_scale("default").n_cards == 200_000 and get_scale("enormous").n_cards == 2_000_000
    with pytest.raises(ValueError):
        get_scale("huge")


@pytest.mark.parametrize("table,model", [("wells", S.Well), ("cycles", S.Cycle), ("cycle_daily", S.CycleDaily),
                                          ("failures", S.Failure), ("unseats", S.Unseat),
                                          ("workovers", S.Workover), ("optimiser_traces", S.OptimiserTrace)])
def test_tables_validate(tables, table, model):
    df = tables[table]
    assert len(df) > 0
    assert set(df["source"]) == {"physics_synthetic"}
    assert S.validate_frame(model, df, sample=None if len(df) < 3000 else 3000) > 0


def test_telemetry_and_cards_validate(built):
    syn = built["syn"]
    files = sorted((syn / "telemetry").glob("*/*.parquet"))
    assert len(files) == 2
    t = pd.read_parquet(files[0]).head(200)
    t["well_id"] = files[0].parent.name.split("=")[1]
    t["label"] = t["label"].astype(str)
    for r in t.to_dict("records"):
        r = {k: (None if isinstance(v, float) and v != v else v) for k, v in r.items()}
        if r["load_kn"] is None:
            continue
        S.TelemetryRow.model_validate(r)
    cards = pd.read_parquet(syn / "dyno_cards" / "part-000.parquet")
    assert len(cards) == 1200
    row = cards.iloc[3].to_dict()
    for c in s4_cards.ARRAY_COLS:
        assert len(row[c]) == 128 and np.asarray(row[c]).dtype == np.float32
        row[c] = [float(x) for x in row[c]]
    S.DynoCard.model_validate(row)


def test_cards_balanced_classes_and_finite(built):
    cards = pd.read_parquet(built["syn"] / "dyno_cards" / "part-000.parquet")
    counts = cards["label"].value_counts()
    assert set(counts.index) == set(DYNO_CLASSES) and counts.min() == counts.max() == 100
    assert set(cards["augmentation"]) <= set(s4_cards.AUGMENTATIONS)
    assert np.isfinite(np.stack(cards["surface_load"])).all() and np.isfinite(np.stack(cards["downhole_pos"])).all()


def test_determinism_all_stages():
    w1, w2 = s1_roster.generate("small"), s1_roster.generate("small")
    assert frame_hash(w1) == frame_hash(w2)
    c1, d1 = s2_cycles.generate(w1, "small")
    c2, d2 = s2_cycles.generate(w2, "small")
    assert frame_hash(c1) == frame_hash(c2) and frame_hash(d1) == frame_hash(d2)
    f1 = s5_failures.generate(w1, c1, d1)
    f2 = s5_failures.generate(w2, c2, d2)
    assert all(frame_hash(a) == frame_hash(b) for a, b in zip(f1, f2, strict=True))
    assert frame_hash(s6_traces.generate(w1, "small")) == frame_hash(s6_traces.generate(w1, "small"))
    a = s4_cards.generate("small")
    assert frame_hash(a) == frame_hash(s4_cards.generate("small"))
    tw = w1.iloc[0].to_dict()
    assert frame_hash(s3_telemetry.generate_well(tw, 1)[0].head(5000)) == frame_hash(
        s3_telemetry.generate_well(tw, 1)[0].head(5000))
    assert frame_hash(s1_roster.generate("small", seed=1)) != frame_hash(w1)


def test_showcase_reproduces_frontend_defaults(tables):
    w = tables["wells"].set_index("well_id").loc["BGW-17"]
    assert w["is_showcase"] and w["pi_factor"] == 1 and w["visc_factor"] == 1 and w["steam_eff"] == 1
    cyc = tables["cycles"].query("well_id == 'BGW-17'").set_index("cycle_no")
    cur = cyc.loc[4]
    assert (cur["spm"], cur["kd"], cur["steam_t"]) == (5.4, 0.5, 800.0) and not cur["complete"]
    assert list(cyc.loc[[1, 2, 3], "cum_oil_bbl"].round()) == [3900.0, 3500.0, 3150.0]
    d = tables["cycle_daily"].query("well_id == 'BGW-17' and cycle_no == 4")
    assert d["day"].max() == 41
    m = WellSim().metrics()             # frontend defaults: spm 5.4, kd 0.5, steam 800, day 41
    r = d[d.day == 41].iloc[0]
    assert r["oil_bpd"] == pytest.approx(m.oil_rate, rel=1e-9)
    assert r["sandface_t_c"] == pytest.approx(m.sandface_t, rel=1e-9)
    assert r["viscosity_cp"] == pytest.approx(m.viscosity, rel=1e-9)
    assert r["fillage"] == pytest.approx(m.fillage, rel=1e-9)
    assert r["motor_kw"] == pytest.approx(m.motor_kw, rel=1e-9)
    assert r["water_cut"] == pytest.approx(m.water_cut, rel=1e-9)
    assert r["float_margin"] == pytest.approx(m.float_margin, rel=1e-9)


def test_cycle_physical_sanity(tables):
    d, c = tables["cycle_daily"], tables["cycles"]
    assert d["fillage"].between(0, 1).all() and d["water_cut"].between(0, 1).all()
    assert (d["oil_bpd"] >= 0).all() and (d["viscosity_cp"] > 0).all()
    assert (c["sor"] > 0).all() and (c["cum_oil_bbl"] > 0).all()
    inj = d[d.phase == "INJECTION"]
    assert (inj["oil_bpd"] == 0).all() and (inj["net_inr"] < 0).all()
    # cycle totals equal the sum of the daily rows
    tot = d.groupby(["well_id", "cycle_no"])["oil_bpd"].sum()
    for r in c.itertuples():
        assert tot[(r.well_id, r.cycle_no)] == pytest.approx(r.cum_oil_bbl)
    # exactly one in-progress cycle per well, the latest one
    assert (c.groupby("well_id")["complete"].apply(lambda s: (~s).sum()) == 1).all()


def test_failures_only_where_hazard_positive(tables):
    f, c, d = tables["failures"], tables["cycles"], tables["cycle_daily"]
    rods = f[f.kind == "rod_part"]
    assert len(rods) > 0
    assert (rods["goodman"] > 0).all()
    assert (rod_damage_rate(rods["goodman"].to_numpy(), 5.0 * 1440) > 0).all()
    assert rods["rod_index"].between(0, 139).all() and rods["depth_m"].between(0, 1100).all()
    assert set(rods["mode"]) <= {"fatigue", "float-buckling"}
    # every failure falls inside its cycle's production window
    cyc = c.set_index(["well_id", "cycle_no"])
    dd = d[d.phase == "PRODUCTION"].groupby(["well_id", "cycle_no"])["date"].agg(["min", "max"])
    for r in f.itertuples():
        lo, hi = dd.loc[(r.well_id, r.cycle_no)]
        assert lo <= r.date <= hi, (r, cyc.loc[(r.well_id, r.cycle_no)]["start_date"])
    assert (f["cost_inr"] > 0).all() and (f["downtime_h"] > 0).all()


def test_unseats_and_workovers_consistent(tables):
    u, wo = tables["unseats"], tables["workovers"]
    assert (u["uplift_kn"] > 0).all()
    assert (u["uplift_kn"] > 0.5 * u["hold_down_kn"]).all()        # hazard is negligible far below capacity
    for trig, key in (("pump_unseat", "unseat_id"), ("rod_part", "failure_id")):
        ids = set(wo.query("trigger == @trig")["trigger_id"].dropna().astype(int))
        src = tables["unseats"] if trig == "pump_unseat" else tables["failures"].query("kind == 'rod_part'")
        assert ids == set(src[key])


def test_unseat_rates_are_realistic(tables):
    """Heavy-oil insert pump on a mechanical hold-down: ~0-4 unseats per well-year, never a cluster on consecutive days."""
    from mantle_physics.hazard import UNSEAT_LOCKOUT_DAYS

    u, d = tables["unseats"].copy(), tables["cycle_daily"]
    u["date"] = pd.to_datetime(u["date"])
    for _, g in u.groupby("well_id"):
        gaps = g["date"].sort_values().diff().dropna().dt.days
        assert (gaps >= UNSEAT_LOCKOUT_DAYS).all()
    well_years = (d["phase"] == "PRODUCTION").sum() / 365.0
    assert len(u) / well_years < 2.0                                   # fleet mean
    yr = u.groupby(["well_id", u["date"].dt.year]).size()
    assert yr.max() <= 4 if len(yr) else True


def test_telemetry_labels_align_with_injected_windows(built):
    syn = built["syn"]
    ev = pd.read_parquet(syn / "telemetry_events.parquet")
    assert set(ev["label"]) == {"pump_off", "gas_lock", "load_cell_fault", "vfd_trip"} | (
        {"tubing_leak_onset"} & set(ev["label"]))
    for wid, g in ev.groupby("well_id"):
        t = pd.read_parquet(syn / "telemetry" / f"well_id={wid}" / "part-0.parquet")
        t["label"] = t["label"].astype(str)
        assert t["ts"].is_monotonic_increasing and t["ts"].diff().dropna().eq(pd.Timedelta(seconds=1)).all()
        labelled = pd.Series("normal", index=t.index)
        for e in g.itertuples():
            m = (t["ts"] >= e.start_ts) & (t["ts"] < e.end_ts)
            assert m.sum() == pytest.approx(e.duration_s, abs=1)
            labelled[m] = e.label
        assert (labelled == t["label"]).all()
        # signatures: a VFD trip stops the motor
        for e in g[g.label == "vfd_trip"].itertuples():
            w = t[(t["ts"] >= e.start_ts) & (t["ts"] < e.end_ts)].dropna(subset=["vfd_hz"])
            assert (w["vfd_hz"] == 0).all() and (w["amps"] == 0).all()
        # normal rows are running: positive VFD, sane pos range, dropout NaNs are the only gaps
        norm = t[t["label"] == "normal"].dropna(subset=["vfd_hz"])
        assert (norm["vfd_hz"] > 5).all() and norm["pos_m"].between(-0.01, 3.1).all()
        assert t["load_kn"].isna().mean() < 0.02


def test_telemetry_sensor_imperfections_present(built):
    t = pd.read_parquet(next((built["syn"] / "telemetry").glob("*/*.parquet")))
    assert t["load_kn"].isna().any()                          # dropouts
    norm = t[t.label == "normal"]["load_kn"].dropna()
    assert norm.max() > norm.median() * 1.5                   # load swings over the stroke


def test_traces_sane(tables):
    t = tables["optimiser_traces"]
    assert t["action_spm"].between(2, 9).all() and t["action_kd"].between(0.4, 0.7).all()
    assert t["outcome_mean_fillage"].between(0, 1).all() and (t["outcome_cum_oil_bbl"] > 0).all()
    assert t["trace_id"].is_unique
