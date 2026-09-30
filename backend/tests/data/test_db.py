from __future__ import annotations

from datetime import date

import pandas as pd
import pytest
from typer.testing import CliRunner

from mantle_data import db
from mantle_data.cli import app


def test_round_trip_counts_match_parquet(built):
    counts = db.stats(built["db"])
    syn = built["syn"]
    for name in ("wells", "cycles", "cycle_daily", "failures", "unseats", "workovers", "optimiser_traces"):
        assert counts[name] == len(pd.read_parquet(syn / f"{name}.parquet")), name
    assert counts["telemetry"] == 2 * 86400
    assert counts["dyno_cards"] == 1200
    assert counts["telemetry_events"] == len(pd.read_parquet(syn / "telemetry_events.parquet"))


def test_reload_is_idempotent(built):
    a = db.load(synthetic=built["syn"])
    b = db.load(synthetic=built["syn"])
    assert a == b


def test_get_well_and_cycles(built):
    with db.MantleDB(built["db"]) as m:
        w = m.get_well("BGW-17")
        assert w["is_showcase"] and w["api"] == 18.0 and m.get_well("BGW-99") is None
        assert len(m.wells()) == 20
        c = m.well_cycles("BGW-17")
        assert list(c["cycle_no"]) == [1, 2, 3, 4] and list(c["complete"]) == [True, True, True, False]
        d = m.cycle_daily("BGW-17", 4)
        assert d["day"].tolist() == list(range(42)) and d["day"].is_monotonic_increasing
        assert d.iloc[41]["oil_bpd"] > 0


def test_failures_unseats_and_past_curves(built):
    with db.MantleDB(built["db"]) as m:
        f = m.failures("BGW-17")
        assert f["date"].is_monotonic_increasing
        assert (f["well_id"] == "BGW-17").all()
        as_of = m.as_of("BGW-17")
        assert as_of == date(2026, 9, 30)
        u12 = m.unseats("BGW-17", months=12)
        u3 = m.unseats("BGW-17", months=3)
        assert len(u3) <= len(u12) <= len(m.con.execute(
            "SELECT * FROM unseats WHERE well_id='BGW-17'").df())
        if len(u3):
            assert (pd.to_datetime(u3["date"]) > pd.Timestamp(as_of) - pd.DateOffset(months=3)).all()
        assert len(m.unseats("BGW-17", months=12, as_of=date(2000, 1, 1))) == 0
        past = m.past_cycle_curves("BGW-17")
        assert [p["n"] for p in past] == [1, 2, 3]
        assert [round(p["cum_oil"]) for p in past] == [3900, 3500, 3150]
        assert len(past[0]["day"]) == len(past[0]["oil"]) == len(past[0]["T"]) > 60


def test_telemetry_window(built):
    with db.MantleDB(built["db"]) as m:
        w = m.telemetry_window("BGW-17", "2026-08-01 00:00:00", "2026-08-01 00:10:00")
        assert len(w) == 600 and w["ts"].is_monotonic_increasing
        assert {"load_kn", "pos_m", "amps", "kw", "vfd_hz", "thp_mpa", "chp_mpa", "flowline_t_c", "label"} <= set(w)
        assert m.telemetry_window("BGW-17", "2001-01-01", "2001-01-02").empty
        assert set(w["well_id"]) == {"BGW-17"}


def test_dyno_view_readable_and_labels(built):
    with db.MantleDB(built["db"]) as m:
        r = m.con.execute("SELECT label, count(*) c FROM dyno_cards GROUP BY 1").df()
        assert len(r) == 12 and (r["c"] == 100).all()
        n = m.con.execute("SELECT len(surface_load) FROM dyno_cards LIMIT 1").fetchone()[0]
        assert n == 128


def test_cli_db_commands(built, monkeypatch):
    monkeypatch.setenv("MANTLE_DATA_DIR", str(built["root"]))
    r = CliRunner().invoke(app, ["db", "stats"])
    assert r.exit_code == 0 and "wells" in r.output and "telemetry" in r.output


def test_build_only_flag_and_bad_stage(tmp_path, monkeypatch):
    from mantle_data.synth.build import build, parse_only

    monkeypatch.setenv("MANTLE_DATA_DIR", str(tmp_path))
    info = build("small", only="S2,S4", out_dir=tmp_path / "syn", load_db=False, log=lambda *_: None)
    assert set(info["stages"]) == {"S2", "S4"}
    assert (tmp_path / "syn" / "cycles.parquet").exists() and not (tmp_path / "syn" / "failures.parquet").exists()
    with pytest.raises(ValueError):
        parse_only("S9")
