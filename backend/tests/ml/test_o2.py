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
    assert p["joint"]["value_inr"] >= p["sequential"]["value_inr"] - 1e-6
    assert p["coupling_dividend_inr"] >= 0 and p["joint_share"] == p["coupling_dividend_inr"]
    lo, hi = p["p10_p90"]["inr_per_cycle"]
    assert lo <= p["inr_per_cycle"] <= hi
    assert len(p["sor"]) == 2 and p["sor"][1] > 0
    assert p["seconds"] < 6.0


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
