from __future__ import annotations

import numpy as np
import pytest

from mantle_ml import data
from mantle_ml.models import m0_viscosity as m0
from mantle_ml.models import m1_thermal as m1
from mantle_ml.models import m2_forecast as m2
from mantle_ml.models import o2_css as o2


@pytest.fixture(scope="module")
def planner(ml_data, quick_models):
    for mod in (m0, m1, m2):
        mod.train(quick_models, quick=True)
    fm = m2.ForecastModel.load(quick_models / "M2", m1.ThermalModel.load(quick_models / "M1"), m0.ViscosityModel.load(quick_models / "M0"))
    return o2.Planner(fm)


def test_plan_valid_ranges_and_joint_ge_sequential(planner):
    w = data.wells().iloc[2].to_dict()
    p = planner.plan(w, 3, budget_s=1.0)
    for k, (lo, hi) in o2.RANGES.items():
        assert lo <= p["mantle"][k] <= hi
    assert p["joint"]["inr_per_day"] >= p["sequential"]["inr_per_day"] - 1e-6
    assert p["coupling_dividend_inr"] >= 0 and p["joint_share"] == p["coupling_dividend_inr"]
    lo, hi = p["p10_p90"]["inr_per_cycle"]
    assert lo <= p["inr_per_cycle"] <= hi
    assert len(p["sor"]) == 2 and p["sor"][1] > 0
    assert p["seconds"] < 6.0


def _twin_rate(planner, w, plan, fixed):
    return planner.score(w, plan, fixed, exact=True)


def test_cutoff_and_soak_enter_the_objective(planner):
    """Regression: cut-off used to leave the plan at 120 d while the twin's own economic cut-off was ~68 d."""
    w = data.wells().iloc[2].to_dict()
    late = _twin_rate(planner, w, o2.PRACTICE, o2.PRACTICE_PUMP)
    econ = o2._economic_cutoff(w, o2.PRACTICE, o2.PRACTICE_PUMP)
    assert econ < 100                                                    # the twin's rule says re-steam well before day 120
    early = _twin_rate(planner, w, {**o2.PRACTICE, "cutoff": float(econ)}, o2.PRACTICE_PUMP)
    assert early["rate"] > 1.05 * late["rate"] and early["cum_oil"] < late["cum_oil"]      # less oil per cycle, more INR per day
    assert early["days"] < late["days"]
    # soak costs calendar days too: a long soak at equal reservoir benefit is worse per day
    assert o2.cycle_days({**o2.PRACTICE, "soak": 8.0}) == pytest.approx(o2.cycle_days(o2.PRACTICE) + 4.0)


def test_plan_moves_cutoff_toward_the_twin_economic_rule(planner):
    moved = 0
    for i in (2, 3, 4):
        w = data.wells().iloc[i].to_dict()
        p = planner.plan(w, 3, budget_s=1.0)
        m = p["mantle"]
        econ = o2._economic_cutoff(w, m, (p["pump"]["spm"], p["pump"]["kd"]))
        assert abs(m["cutoff"] - econ) <= 12, (m, econ)
        moved += m["cutoff"] < o2.PRACTICE["cutoff"]
    assert moved >= 2


def test_reported_numbers_are_mutually_consistent_on_the_twin(planner):
    """oil lift, SOR pair, INR per cycle, joint share and the plan curve all re-derive from twin runs of the chosen plans."""
    from mantle_physics.economics import sor

    w = data.wells().iloc[3].to_dict()
    p = planner.plan(w, 3, budget_s=1.0)
    pr = _twin_rate(planner, w, o2.PRACTICE, o2.PRACTICE_PUMP)
    jt = _twin_rate(planner, w, p["mantle"], None)
    assert (jt["pump"]["spm"], jt["pump"]["kd"]) == (p["pump"]["spm"], p["pump"]["kd"])
    t_p = pr["days"]
    assert p["inr_per_cycle"] == pytest.approx((jt["rate"] - pr["rate"]) * t_p, rel=1e-6, abs=1.0)
    assert p["oil_lift"] == pytest.approx(jt["oil_per_day"] / pr["oil_per_day"] - 1, rel=1e-6, abs=1e-9)
    assert p["sor"][0] == pytest.approx(sor(800, pr["cum_oil"])) and p["sor"][1] == pytest.approx(sor(p["mantle"]["steam"], jt["cum_oil"]))
    sq = _twin_rate(planner, w, p["sequential"]["plan"], None)
    assert p["joint_share"] == pytest.approx(max(0.0, (jt["rate"] - sq["rate"]) * t_p), rel=1e-6, abs=1.0)
    assert 0 <= p["joint_share"] <= max(p["inr_per_cycle"], 0) + 1.0            # the dividend is part of the total gain
    # sign consistency: more INR per practice-cycle of calendar time never comes with a lower value per day, and vice versa
    assert (p["inr_per_cycle"] > 0) == (jt["rate"] > pr["rate"])
    # the plan curve is the twin's oil for the chosen plan up to its cut-off
    c = p["plan_curve"]
    assert c["day"][0] == 18 and c["day"][-1] == c["cutoff"] == p["mantle"]["cutoff"]
    assert np.trapezoid(c["oil"]) == pytest.approx(jt["cum_oil"], rel=1e-9)
    assert all(lo <= o + 1e-9 <= hi + 2e-9 for lo, o, hi in zip(c["oil_p10"], c["oil"], c["oil_p90"], strict=True))
    assert p["per_cycle"]["mantle_oil_bbl"] == pytest.approx(jt["cum_oil"])


def test_plan_ui_shape_and_cache(planner):
    w = data.wells().iloc[4].to_dict()
    a = planner.plan(w, 2, budget_s=1.0)
    b = planner.plan(w, 2, budget_s=1.0)
    assert a is b                                           # cached per well/cycle
    ui = o2.to_ui(a)
    assert set(ui) == {"practice", "mantle", "ranges", "oilLift", "sor", "inrPerCycle", "jointShare"}
    assert set(ui["practice"]) == {"steam", "pInj", "soak", "cutoff"}


def test_pressure_requirement_monotone():
    assert o2.p_required(900) > o2.p_required(700)
    assert np.isclose(o2.p_required(800), 9.14, atol=0.01)


def test_shipped_o2(shipped):
    m = shipped("O2")["metrics"]
    assert m["joint_ge_sequential_all"] and m["ranges_valid_all"] and m["seconds_max"] < 6.0
    assert m["gain_vs_practice_inr_mean_twin_verified"] > 0
