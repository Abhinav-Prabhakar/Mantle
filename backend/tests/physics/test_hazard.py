"""Hazard model tests: monotone in stress and impacts, negligible at low stress."""

from __future__ import annotations

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from mantle_physics import (
    WellSim,
    pump_unseat_hazard,
    pump_uplift_kn,
    rod_damage_rate,
    rod_hazard_rate,
    simulate_rod_failures,
)
from mantle_physics.hazard import (
    goodman_ratio,
    rod_failure_probability,
    rod_stress_by_depth,
)

SPD = 7800.0


@given(st.floats(0.05, 1.4), st.floats(0.05, 1.4))
def test_damage_monotone_in_goodman(a, b):
    lo, hi = min(a, b), max(a, b)
    assert rod_damage_rate(lo, SPD) <= rod_damage_rate(hi, SPD)


def test_damage_monotone_in_every_driver():
    base = {"goodman": 0.7, "strokes_per_day": SPD, "float_frac": 0.0, "impacts_per_day": 0.0, "impact_vel": 0.0, "corrosion": 0.0}
    r0 = rod_damage_rate(**base)
    for key, val in [("strokes_per_day", 2 * SPD), ("float_frac", 0.2), ("impacts_per_day", 3000.0), ("corrosion", 0.5)]:
        assert rod_damage_rate(**{**base, key: val}) > r0
    imp = {**base, "impacts_per_day": 3000.0}
    assert rod_damage_rate(**{**imp, "impact_vel": 1.0}) > rod_damage_rate(**imp)


def test_low_stress_is_negligible():
    r = rod_damage_rate(0.3, SPD)
    assert r * 365 < 1e-3
    assert rod_hazard_rate(r * 365, r) < 1e-6


def test_hazard_monotone_in_damage_and_rate():
    d = np.linspace(0.01, 2, 50)
    h = rod_hazard_rate(d, 1e-3)
    assert np.all(np.diff(h) > 0)
    assert np.all(np.diff(rod_hazard_rate(0.5, np.linspace(1e-4, 1e-2, 20))) > 0)
    assert rod_failure_probability(0.1, 1e-3, 30) < rod_failure_probability(0.1, 1e-3, 300) <= 1


def test_goodman_ratio_matches_twin_and_profile_stress():
    sim = WellSim(spm=5.4, cycle_day=41)
    m = sim.metrics()
    prof = sim.profile()
    # the twin's top-of-string Goodman uses smin>=0; with smin = 0 it reduces to smax/(0.85*T/4)
    smax = prof.rod_stress[0]
    assert abs(goodman_ratio(smax, 0.0) - smax / (0.85 * 793 / 4)) < 1e-12
    assert 0 < goodman_ratio(smax, 0.0) < 2
    assert m.goodman > 0
    stress = rod_stress_by_depth([0, 400, 900], 7800.0, 0.05, 0.0, 0.0)
    assert stress[0] > stress[1] > stress[2] > 0


def test_pump_uplift_and_unseat_hazard_monotone():
    mus = np.linspace(100, 8000, 10)
    up = pump_uplift_kn(mus, 0.3, 0.9)
    assert np.all(np.diff(up) > 0)
    assert pump_uplift_kn(1000, 0.6, 0.9) > pump_uplift_kn(1000, 0.3, 0.9)
    assert pump_uplift_kn(1000, 0.3, 0.4) > pump_uplift_kn(1000, 0.3, 0.9)
    assert pump_uplift_kn(1000, 0.3, 0.4, impact_vel=1.0) > pump_uplift_kn(1000, 0.3, 0.4)
    h = pump_unseat_hazard(np.linspace(1, 40, 30))
    assert np.all(np.diff(h) > 0)
    assert pump_unseat_hazard(4.0) < 1e-4                        # low uplift: negligible
    assert pump_unseat_hazard(18.0) > pump_unseat_hazard(18.0, hold_down_kn=30.0)


def test_simulated_failures_scale_with_stress():
    rng = np.random.default_rng(0)
    assert simulate_rod_failures(rng, 0.3, SPD, 365) == []
    hi = simulate_rod_failures(np.random.default_rng(1), 0.95, SPD, 365, float_frac=0.2)
    mid = simulate_rod_failures(np.random.default_rng(1), 0.8, SPD, 365)
    assert len(hi) > len(mid) >= 0
    assert [f.day for f in hi] == sorted(f.day for f in hi)
    assert {f.mode for f in hi} <= {"fatigue", "float-buckling"}
    again = simulate_rod_failures(np.random.default_rng(1), 0.95, SPD, 365, float_frac=0.2)
    assert [(f.day, f.rod) for f in hi] == [(f.day, f.rod) for f in again]
    per_rod = np.linspace(0.4, 1.0, 140)                         # stress rising with depth -> lower rods fail
    f = simulate_rod_failures(np.random.default_rng(2), per_rod, SPD, 730)
    assert f and np.mean([x.rod for x in f]) > 70
