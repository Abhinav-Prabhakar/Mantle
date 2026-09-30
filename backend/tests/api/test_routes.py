from __future__ import annotations

import math

import pytest

from mantle_physics import WellSim

W = "/api/wells/BGW-17"


def test_health_meta(client):
    h = client.get("/api/health").json()
    assert h["status"] == "ok" and set(h["models_loaded"]) >= {"M0", "M1", "M2", "M3", "M4", "M5", "M6", "O1", "O2"}
    m = client.get("/api/meta").json()
    assert m["data_source"] == "physics_synthetic"
    assert {"oil_inr_bbl", "steam_inr_t", "power_inr_kwh"} == set(m["prices"])
    ids = {x["id"] for x in m["models"]}
    assert {"M0", "M3", "M6", "O2"} <= ids
    assert all(x["licence"] for x in m["sources"]) and any(x["kind"] == "real" for x in m["sources"])
    assert next(x for x in m["models"] if x["id"] == "M3")["metrics"]["value"] > 0


def test_wells_roster_and_detail(client):
    ws = client.get("/api/wells").json()
    assert len(ws) == 60 and ws[0]["id"] == "BGW-01"
    w = next(x for x in ws if x["id"] == "BGW-17")
    assert (w["cycle"], w["cycle_day"], w["phase"]) == (4, 41, "PRODUCTION")
    d = client.get(W).json()
    assert d["field"] == "Baghewala" and d["reservoir"] == "Jodhpur Sandstone"
    assert d["fluid"]["t_res"] == 47 and 1e4 < d["fluid"]["dead_oil_cp"] < 3e4       # M0 at reservoir temperature
    assert d["unit"]["gearbox_rating_inlb"] == 320000 and d["completion"]["plunger_in"] == 1.25
    r = d["rods"]
    assert r["count"] == 140 and r["length_m"] == pytest.approx(7.62) and r["tapers"][-1]["to"] == 1068
    assert d["unit"]["model"].startswith("C-") and d["unit"]["stroke_m"] == pytest.approx(3.0255, abs=1e-3)


def test_state_units_and_sanity(client):
    s = client.get(f"{W}/state?day=41&spm=5.4&kd=0.5&steam=800").json()
    assert s["params"] == {"day": 41, "spm": 5.4, "kd": 0.5, "steam": 800} and s["source"] == "physics_synthetic"
    m, d, r = s["metrics"], s["derived"], s["recommendation"]
    assert m["phase"] == "PRODUCTION" and 0 < m["fillage"] < 1 and 20 < m["oilRate"] < 120
    assert r["model"] == "O1" and r["spm"] > 0 and set(r["deltas"]) == {"oil", "float", "energy", "impacts"}
    assert d["hz"] == pytest.approx(5.4 * 50 / 9)
    c = d["cost"]
    assert c["costDay"] == pytest.approx(c["steamDay"] + c["powerDay"] + c["maintDay"] + c["chemDay"])
    assert c["revenueDay"] == pytest.approx(m["oilRate"] * 6000)
    assert c["maintDay"] > 0                                  # from the recorded workovers
    assert 0 < d["recovery"] < 0.1 and d["pRes"] == pytest.approx(3.1)
    assert 0 <= d["unseatRisk"] <= 1 and d["impactsDay"] >= 0 and d["impactsMantle"] <= d["impactsDay"]
    assert len(d["profile"]) == 36


def test_maint_cost_follows_recorded_workovers(client, engine):
    wd = engine.store.well("BGW-17")
    from mantle_api.store import maint_per_day
    exp = maint_per_day(wd, wd.scenario_date(41), 365)
    s = client.get(f"{W}/state").json()
    assert s["derived"]["cost"]["maintDay"] == pytest.approx(exp)
    other = client.get("/api/wells/BGW-03/state").json()["derived"]["cost"]["maintDay"]
    assert other != pytest.approx(exp)                        # each well has its own workover record


def test_state_phases(client):
    inj = client.get(f"{W}/state?day=5").json()
    assert inj["metrics"]["phase"] == "INJECTION" and inj["derived"]["impactsDay"] == 0
    assert inj["derived"]["cost"]["costBbl"] is None and inj["metrics"]["steamTons"] == pytest.approx(5 * 800 / 14)
    assert client.get(f"{W}/state?day=16").json()["metrics"]["phase"] == "SOAK"


def test_bgw17_parity_with_wellsim(client):
    m = client.get(f"{W}/state").json()["metrics"]
    assert m == WellSim().metrics().to_json()
    m2 = client.get(f"{W}/state?day=70&spm=6.2&kd=0.58&steam=900").json()["metrics"]
    assert m2 == WellSim(spm=6.2, cycle_day=70, kd=0.58, steam=900).metrics().to_json()


def test_other_well_is_calibrated(client):
    a = client.get("/api/wells/BGW-03/state").json()
    assert a["metrics"]["phase"] in {"INJECTION", "SOAK", "PRODUCTION"}
    b = client.get("/api/wells/BGW-05/state").json()
    assert a["metrics"]["oilRate"] != b["metrics"]["oilRate"]


def test_series(client):
    s = client.get(f"{W}/series?spm=5.4&kd=0.5&steam=800").json()
    assert len(s["day"]) == 121 == len(s["oilP10"]) == len(s["T"])
    assert all(hi >= lo - 1e-9 for hi, lo in zip(s["oilP10"], s["oilP90"], strict=True))       # P10 high, P90 low
    assert s["oilP10"][60] > s["oil"][60] > s["oilP90"][60] > 0 and s["oil"][5] == 0
    assert s["model"] == "M2" and len(s["pastCycles"] if "pastCycles" in s else s["past_cycles"]) == 3
    pc = s["past_cycles"]
    assert [c["n"] for c in pc] == [1, 2, 3] and len(pc[0]["oil"]) == 121
    assert sum(x for x in pc[0]["oil"] if x is not None) == pytest.approx(3900, rel=0.03)      # recorded cycle 1
    curve = s["plan_curve"]
    assert len(curve["day"]) == len(curve["oil"]) > 20 and curve["cutoff"] > 0


def test_profile(client):
    p = client.get(f"{W}/profile?day=41").json()
    n = len(p["depth"])
    assert n == 126 and all(len(p[k]) == n for k in ("Tfluid", "Tformation", "mu", "pressure", "rodStress"))
    assert p["depth"][-1] == 1250 and max(p["Tfluid"]) > 100


def test_dyno(client):
    d = client.get(f"{W}/dyno").json()
    assert len(d["surface"]) == len(d["downhole"]) == 128 and d["cls"] and 0 < d["clsConf"] <= 1
    assert d["model"] == "M3" and sum(d["class_probs"].values()) == pytest.approx(1, abs=1e-3) and len(d["class_probs"]) == 12
    assert d["cls_id"] in d["class_probs"] and d["xMax"] == pytest.approx(3.0255, abs=1e-3)
    if d["impact"]:
        assert 0 <= d["impact"]["x"] <= d["xMax"]


def test_health_rods(client):
    h = client.get(f"{W}/health").json()
    assert len(h["rods"]) == 140 and [r["index"] for r in h["rods"]] == list(range(140))
    assert h["rods"][0]["taper"] == "1⅛″" and h["rods"][-1]["taper"] == "⅞″"
    assert h["failure_window_months"] == 12 and len(h["unseats"]["months"]) == 12
    assert {f["rod"] for f in h["failures"]} == {r["index"] for r in h["rods"] if r["failed"]}
    for f in h["failures"]:
        assert set(f) >= {"rod", "depth", "size", "mode", "date", "cause"}
    assert len(h["unseats"]["events"]) == len(h["unseats"]["details"]) and h["unseats"]["hold_down_kn"] > 0
    assert 0 <= h["rod_risk_30d"] <= 1 and 0 <= h["unseat_risk_30d"] <= 1 and h["model"] == "M4"
    assert h["mtbf_days"] > 0 and h["mtbf_mantle_days"] > 0 and h["uplift_margin"] > 0


def test_health_failures_match_database(client, engine):
    wd = engine.store.well("BGW-17")
    h = client.get(f"{W}/health").json()          # as of the last recorded day
    rods = wd.failures[wd.failures.kind == "rod_part"]
    recent = rods[rods.date >= "2025-09-30"]
    assert len(h["failures"]) == len(recent)
    n_un = len(wd.unseats[wd.unseats.date > "2025-09-30"])
    assert len(h["unseats"]["events"]) == n_un


def test_plan_is_coherent_with_the_twin(client):
    """Regression: plan kept cut-off 120 (twin economic cut-off ~68), showed oil lift -2 % with +INR, and an SOR pair that was
    not on the twin's sor basis. Every number must re-derive from the twin; the plan curve is that plan's curve."""
    from mantle_data.synth.wellmodel import soak_factor
    from mantle_physics.economics import sor

    p = client.get(f"{W}/plan/next-cycle").json()
    curve = client.get(f"{W}/series").json()["plan_curve"]
    m, pr, pc, pump = p["mantle"], p["practice"], p["per_cycle"], p["pump"]
    # the cut-off is a real lever: it moves to the twin's own economic cut-off for the plan (state metric daysToCutoff)
    st = client.get(f"{W}/state?day=41&spm={pump['spm']}&kd={pump['kd']}&steam={int(m['steam'])}").json()["metrics"]
    econ = 41 + st["daysToCutoff"]
    assert m["cutoff"] <= pr["cutoff"] - 20 and abs(m["cutoff"] - econ) <= 8
    assert 2 <= m["soak"] <= 10 and 500 <= m["steam"] <= 1200
    # SOR pair = the twin's sor metric at each plan's cut-off day (same steam/oil basis as the UI KPI)
    s_pr = client.get(f"{W}/state?day={int(pr['cutoff'])}&spm={pump['practice_spm']}&kd={pump['practice_kd']}&steam={int(pr['steam'])}").json()["metrics"]
    assert p["sor"][0] == pytest.approx(s_pr["sor"], rel=1e-3) and pc["practice_oil_bbl"] == pytest.approx(s_pr["cumOil"], rel=1e-3)
    s_m = client.get(f"{W}/state?day={int(m['cutoff'])}&spm={pump['spm']}&kd={pump['kd']}&steam={int(m['steam'])}").json()["metrics"]
    cum_m = s_m["cumOil"] * soak_factor(m["soak"])                       # the twin's soak law (the UI twin soaks 4 d)
    assert p["sor"][1] == pytest.approx(sor(m["steam"], cum_m), rel=2e-3) and pc["mantle_oil_bbl"] == pytest.approx(cum_m, rel=2e-3)
    # oil lift / INR per cycle / joint share are mutually consistent
    lift = (pc["mantle_oil_bbl"] / pc["mantle_days"]) / (pc["practice_oil_bbl"] / pc["practice_days"]) - 1
    assert p["oil_lift"] == pytest.approx(lift, abs=2e-3)                  # the wire rounds to 3-4 decimals
    assert p["inr_per_cycle"] == pytest.approx((pc["mantle_inr_per_day"] - pc["practice_inr_per_day"]) * pc["practice_days"], rel=1e-3)
    assert (p["oil_lift"] > 0) == (p["inr_per_cycle"] > 0) and 0 <= p["joint_share"] <= p["inr_per_cycle"]
    lo, hi = p["p10_p90"]["inr_per_cycle"]
    assert lo <= p["inr_per_cycle"] <= hi
    # /series plan_curve is the plan's own curve: twin days 18..cut-off, integrating to the reported oil
    assert curve["cutoff"] == m["cutoff"] and curve["day"][0] == 18 and curve["day"][-1] == m["cutoff"]
    assert sum((a + b) / 2 for a, b in zip(curve["oil"], curve["oil"][1:], strict=False)) == pytest.approx(pc["mantle_oil_bbl"], rel=1e-4)
    assert all(hi >= o >= lo - 1e-9 for lo, o, hi in zip(curve["oil_p90"], curve["oil"], curve["oil_p10"], strict=True))   # P10 high


def test_mtbf_improvement_is_defensible(client):
    """Was 159 -> 1169 d (7.4x): the unseat hazard vanished from the MTBF and spm-independent history moved with the setting."""
    h = client.get(f"{W}/health").json()
    r = h["mtbf_ratio"]
    assert r == pytest.approx(h["mtbf_mantle_days"] / h["mtbf_days"], rel=1e-9)
    assert 1.0 <= r <= 3.0
    lo, hi = h["mtbf_ratio_p10_p90"]
    assert lo <= hi and lo >= 1.0 and hi <= 5.0                       # the fold-ensemble spread is reported with the number
    assert h["mtbf_days_p10_p90"][0] <= h["mtbf_days"] * 1.5 and h["mtbf_mantle_days_p10_p90"][1] >= h["mtbf_mantle_days"] * 0.6
    assert isinstance(h["mtbf_extrapolated"], list)


def test_unseat_history_is_realistic(client, engine):
    """BGW-17 showed 35 unseats in 12 months; a heavy-oil insert pump with a mechanical hold-down sees ~0-4 a year."""
    h = client.get(f"{W}/health").json()
    assert len(h["unseats"]["events"]) <= 4
    con = engine.store.con if hasattr(engine.store, "con") else None
    if con is not None:
        rows = con.execute(
            "SELECT well_id, date_part('year', date) y, count(*) n FROM unseats GROUP BY 1, 2").fetchall()
        assert rows and max(r[2] for r in rows) <= 4
        n_un = con.execute("SELECT count(*) FROM unseats").fetchone()[0]
        n_days = con.execute("SELECT sum(n_days) FROM cycles").fetchone()[0]
        assert n_un / (n_days / 365.0) < 2.0                           # fleet unseats per well-year


def test_recommend_and_plan(client):
    r = client.get(f"{W}/recommend/pump").json()
    assert r["model"] == "O1" and 0.5 <= r["spm"] <= 15
    p = client.get(f"{W}/plan/next-cycle").json()
    for side in ("practice", "mantle"):
        assert set(p[side]) >= {"steam", "p_inj", "soak", "cutoff", "inj_days"}
        assert p[side]["inj_days"] == pytest.approx(p[side]["steam"] / p["steam_rate_t_per_d"], abs=0.01)
    lo, hi = p["ranges"]["steam"]
    assert lo <= p["mantle"]["steam"] <= hi and p["cycle"] == 5 and p["model"] == "O2"
    assert len(p["sor"]) == 2 and len(p["p10_p90"]["inr_per_cycle"]) == 2
    assert all(math.isfinite(p[k]) for k in ("oil_lift", "inr_per_cycle", "joint_share"))


def test_errors(client):
    assert client.get("/api/wells/NOPE").status_code == 404
    assert client.get("/api/wells/NOPE/state").status_code == 404
    assert client.get(f"{W}/state?spm=99").status_code == 422
    assert client.get(f"{W}/state?day=-1").status_code == 422
    assert client.get(f"{W}/state?kd=abc").status_code == 422
    assert client.get(f"{W}/series?steam=10").status_code == 422
    assert client.post(f"{W}/apply", json={"spm": 40, "kd": 0.5}).status_code == 422
    assert client.post(f"{W}/apply", json={}).status_code == 422
    assert client.post("/api/wells/NOPE/apply", json={"spm": 4, "kd": 0.5}).status_code == 404


def test_apply_and_schedule_persist(client, engine):
    a = client.post(f"{W}/apply", json={"spm": 4.6, "kd": 0.52}).json()
    assert a["applied"] is True and a["audit_id"].startswith("AUD-") and a["at"]
    s = client.post(f"{W}/plan/schedule", json={"steam": 900, "p_inj": 9.5, "soak": 5, "cutoff": 100}).json()
    assert s["scheduled"] is True and s["cycle"] == 5 and s["audit_id"] != a["audit_id"]
    rows = engine.store.audit_rows("BGW-17")
    assert {a["audit_id"], s["audit_id"]} <= set(rows["audit_id"])
    row = rows[rows.audit_id == s["audit_id"]].iloc[0]
    assert row["action"] == "schedule_plan" and '"steam": 900' in row["payload"] and row["ts"] is not None


def test_cors(client):
    r = client.get("/api/health", headers={"Origin": "http://localhost:8777"})
    assert r.headers["access-control-allow-origin"] == "http://localhost:8777"
    r = client.get("/api/health", headers={"Origin": "http://evil.example"})
    assert "access-control-allow-origin" not in r.headers
