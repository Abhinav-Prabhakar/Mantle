"""Property / sanity tests for the twin (hypothesis)."""

from __future__ import annotations

import math

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from mantle_physics import CYCLE, WellSim, derive, rig, viscosity_cp
from mantle_physics.constants import PRICE, SOAK_END
from mantle_physics.rods import kd_table

FAST = settings(max_examples=25, deadline=None)


@given(st.floats(-50, 400), st.floats(-50, 400))
def test_viscosity_monotone_decreasing(t1, t2):
    lo, hi = min(t1, t2), max(t1, t2)
    assert viscosity_cp(lo) >= viscosity_cp(hi) - 1e-12


def test_viscosity_anchor_points():
    assert viscosity_cp(50) == np.float64(viscosity_cp(50))
    assert abs(viscosity_cp(50) - 12000) / 12000 < 0.02
    assert abs(viscosity_cp(150) - 80) / 80 < 0.02
    assert viscosity_cp(float("nan")) == viscosity_cp(47)     # non-finite falls back to reservoir T
    assert viscosity_cp(1e9) == viscosity_cp(320)             # clamp


@given(st.floats(0, 2 * math.pi))
def test_unit_pose_closes_linkage(theta):
    p = rig.unit_pose(theta)
    U = rig.UNIT
    pitman = math.hypot(p.equalizer["x"] - p.crank_pin["x"], p.equalizer["y"] - p.crank_pin["y"])
    assert abs(pitman - U["P"]) < 1e-9
    rear = math.hypot(p.equalizer["x"] - U["saddle"]["x"], p.equalizer["y"] - U["saddle"]["y"])
    assert abs(rear - U["C"]) < 1e-12
    assert 0 <= rig.rod_position(theta) <= rig.STROKE.length + 1e-5


def test_stroke_geometry():
    assert 2.5 < rig.STROKE.length < 3.5
    assert rig.STROKE.top_y > rig.STROKE.bottom_y


@given(st.floats(0, rig.TRUE_TD))
def test_depth_y_inverse(d):
    y = rig.depth_to_y(d)
    assert -29.0 - 1e-9 <= y <= 1e-9
    assert abs(rig.y_to_depth(y) - d) < 1e-6


@given(st.floats(0, 1250), st.floats(0, 1250))
def test_depth_to_y_monotone(a, b):
    lo, hi = min(a, b), max(a, b)
    assert rig.depth_to_y(lo) >= rig.depth_to_y(hi) - 1e-12


@FAST
@given(st.floats(2, 9), st.floats(0, 120), st.floats(0.4, 0.7), st.floats(400, 1200))
def test_fillage_and_metrics_bounded(spm, day, kd, steam):
    m = WellSim(spm=spm, cycle_day=day, kd=kd, steam=steam).metrics()
    assert 0 <= m.fillage <= 1
    assert 0 <= m.pump_eff <= 1
    assert -1 <= m.float_margin <= 1
    assert 0 <= m.goodman <= 1.5
    assert m.oil_rate >= 0 and m.liquid_rate >= m.oil_rate
    assert 0 <= m.water_cut < 0.4
    assert 0 <= m.thermal_battery <= 1
    assert m.sandface_t >= 47 - 1e-9
    assert m.submergence >= 0


@FAST
@given(st.floats(25, 118), st.floats(0.4, 0.7), st.sampled_from([600, 800, 1000]))
def test_float_margin_sign_flips_at_spm_safe(day, kd, steam):
    sim = WellSim(spm=5, cycle_day=day, kd=kd, steam=steam)
    safe = sim.metrics().spm_safe
    if not 0.8 < safe < 13:
        return
    below, above = 0.9 * safe, 1.1 * safe
    sim.set(spm=below)
    m_lo = sim.metrics()
    sim.set(spm=above)
    m_hi = sim.metrics()
    assert m_lo.spm_safe == m_hi.spm_safe                    # spmSafe does not depend on spm
    assert m_lo.float_margin > 0.15 > m_hi.float_margin
    sim.set(spm=safe)
    assert abs(sim.metrics().float_margin - 0.15) < 1e-9     # margin is exactly the 15 % requirement


def test_float_margin_monotone_in_spm():
    sim = WellSim(cycle_day=90)
    prev = 2.0
    for spm in np.arange(2, 9.01, 0.5):
        sim.set(spm=float(spm))
        fm = sim.metrics().float_margin
        assert fm <= prev + 1e-12
        prev = fm
    assert prev < 0


def test_oil_declines_and_cumulative_consistent():
    sim = WellSim(spm=5.4)
    s = sim.series()
    assert s.oil[SOAK_END + 2] > s.oil[110] > 0
    assert all(s.oil[d] == 0 for d in range(SOAK_END))
    # cumOil at day 120 equals the trapezoid integral of the daily oil curve
    sim.set(cycle_day=120)
    trapz = sum((s.oil[d - 1] + s.oil[d]) / 2 for d in range(SOAK_END + 1, 121))
    assert abs(sim.metrics().cum_oil - trapz) < 1e-9 * max(1, trapz)
    prev = 0.0
    for d in range(SOAK_END, 121, 3):
        sim.set(cycle_day=d)
        c = sim.metrics().cum_oil
        assert c >= prev
        prev = c


def test_energy_economics_sanity():
    sim = WellSim(spm=5.4, cycle_day=41)
    m = sim.metrics()
    assert m.motor_kw > 0.5
    assert abs(m.kwh_per_bbl - m.motor_kw * 24 / max(m.oil_rate, 0.5)) < 1e-9
    expect_net = m.oil_rate * PRICE["oil"] - PRICE["steamT"] * m.steam_tons / (CYCLE["days"] - SOAK_END) - m.motor_kw * 24 * PRICE["kwh"]
    assert abs(m.net_per_day - expect_net) < 1e-6
    assert m.net_per_day > 0
    # more speed -> more power
    sim.set(spm=8)
    assert sim.metrics().motor_kw > m.motor_kw
    # injection has negative daily value, soak zero
    sim.set(cycle_day=7)
    assert sim.metrics().net_per_day < 0
    sim.set(cycle_day=16)
    assert sim.metrics().net_per_day == 0
    assert sim.metrics().oil_rate == 0


def test_sor_falls_and_co2_bounded():
    sim = WellSim()
    sors = []
    for d in (30, 60, 100, 120):
        sim.set(cycle_day=d)
        m = sim.metrics()
        sors.append(m.sor)
        assert 0 < m.co2_per_bbl <= 400
    assert sors == sorted(sors, reverse=True)


def test_coupling_dividend_nonnegative():
    cd = WellSim().metrics().coupling_dividend
    assert cd.inr_per_cycle >= 0 and cd.oil_pct >= 0


def test_recommendation_branches_and_alerts():
    titles, levels = set(), set()
    for spm in (2.5, 5.4, 9):
        for day in (5, 16, 25, 60, 100, 120):
            sim = WellSim(spm=spm, cycle_day=day)
            m = sim.metrics()
            titles.add(m.recommendation.title)
            levels |= {a.level for a in m.alerts}
            assert m.alerts
    assert "Slow down and shape the stroke" in titles
    assert "Match pump speed to inflow" in titles
    assert {"Hold: steaming", "Hold: soak"} <= titles
    assert {"ok", "warn", "crit"} <= levels


def test_phase_stepping_and_state():
    s = WellSim(cycle_day=5, spm=6)
    assert s.state.phase == "INJECTION"
    th0 = s.theta
    for _ in range(100):
        s.step(0.05)
    assert s.theta == th0
    s.set(cycle_day=30)
    assert s.state.phase == "PRODUCTION"
    t1 = s.theta
    for _ in range(200):
        s.step(0.05)
        assert 0 <= s.state.rod_pos <= rig.STROKE.length
    assert s.theta != t1
    s.set(cycle_day=10)
    for _ in range(600):
        s.step(0.05)
    assert s.state.rod_pos > rig.STROKE.length - 0.01 and s.state.spm_actual == 0
    s.step(float("nan"))                                     # non-finite dt is ignored
    assert s.params["kd"] == 0.5


def test_input_clamping():
    s = WellSim(spm=99, cycle_day=999, kd=9, steam=0)
    assert s.params == {"spm": 15.0, "day": 120.0, "kd": 0.7, "steam": 300.0}
    s.set(spm=float("nan"), kd=0.1)
    assert s.params["spm"] == 15.0 and s.params["kd"] == 0.4


def test_dyno_card_shape():
    sim = WellSim(spm=8, cycle_day=100)
    c = sim.dyno_card(60)
    assert len(c.surface) == len(c.downhole) == 60
    assert c.surface[0] == c.surface[-1]
    assert c.f_max > c.f_min
    assert c.cls in {"NORMAL", "FLUID POUND", "ROD FLOAT RISK", "VISCOUS DRAG"}
    j = c.to_json()
    assert set(j) == {"surface", "downhole", "xMax", "fMin", "fMax", "cls", "clsConf"}
    seen = {WellSim(spm=s, cycle_day=d).dyno_card(30).cls for s in (3, 5.4, 9) for d in (25, 60, 110)}
    assert len(seen) >= 2


def test_kd_table_shapes_speed():
    slow_down = kd_table(0.62)
    base = kd_table(0.5)
    assert slow_down.vDn < base.vDn < kd_table(0.4).vDn
    assert kd_table(0.999).kd == 0.75                        # clamp inside the table


def test_derive_fields():
    sim = WellSim()
    d = derive(sim.metrics(), sim.state)
    expected = {
        "hz", "amps", "ampsAvg", "profile", "stroke", "thp", "chp", "pip", "flowT", "pRes", "counterbalance",
        "beamLoad", "impactsDay", "impactsMantle", "impactVel", "uplift", "upliftMargin", "unseatRisk", "cost", "recovery",
    }
    assert set(d) == expected
    assert set(d["cost"]) == {"steamDay", "powerDay", "maintDay", "chemDay", "costDay", "costBbl"}
    assert len(d["profile"]) == 36
    sim.set(cycle_day=5)
    di = derive(sim.metrics(), None)
    assert di["thp"] == 9.4 and di["flowT"] == 285 and di["cost"]["costBbl"] is None
    sim.set(cycle_day=16)
    assert derive(sim.metrics(), None)["chp"] == 1.9


def test_metrics_to_json_keys():
    j = WellSim().metrics().to_json()
    for k in ("phase", "cycleDay", "dayInPhase", "sandfaceT", "heatedRadius", "thermalBattery", "daysToCutoff",
              "oilRate", "waterCut", "liquidRate", "pumpDisplacement", "pumpEff", "floatMargin", "spmSafe",
              "torquePct", "motorKw", "kwhPerBbl", "steamTons", "cumOil", "co2PerBbl", "waterPerBbl",
              "netPerDay", "fluidLevel", "submergence", "couplingDividend", "recommendation", "alerts"):
        assert k in j
    assert set(j["couplingDividend"]) == {"inrPerCycle", "oilPct"}
    p = WellSim().profile().to_json()
    assert {"Tfluid", "Tformation", "depositionTop", "depositionBot", "rodStress"} <= set(p)
    assert len(p["depth"]) == 126
