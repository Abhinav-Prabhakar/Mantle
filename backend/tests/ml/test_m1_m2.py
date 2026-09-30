from __future__ import annotations

import numpy as np

from mantle_ml import data
from mantle_ml.models import m0_viscosity as m0
from mantle_ml.models import m1_thermal as m1
from mantle_ml.models import m2_forecast as m2


def test_m1_quick_shapes(ml_data, quick_models):
    ev = m1.train(quick_models, quick=True)
    assert ev["metrics"]["mae_T_ml"] < 50
    m = m1.ThermalModel.load(quick_models / "M1")
    r = m.predict(800, np.arange(0, 121), soak_d=4)
    assert r["T"].shape == (121,) and np.all(r["T_p10"] <= r["T"] + 1e-9) and np.all(r["T"] <= r["T_p90"] + 1e-9)
    assert np.all((r["battery"] >= 0) & (r["battery"] <= 1)) and r["T"].min() >= 46


def test_m2_quick_forecast(ml_data, quick_models):
    m0.train(quick_models, quick=True)
    m1.train(quick_models, quick=True)
    ev = m2.train(quick_models, quick=True)
    assert ev["metrics"]["n_cycles"] > 0
    model = m2.ForecastModel.load(quick_models / "M2", m1.ThermalModel.load(quick_models / "M1"),
                                  m0.ViscosityModel.load(quick_models / "M0"))
    well = data.wells().iloc[0].to_dict()
    r = model.predict_daily(well, 800, 4, 5.4, 0.5, 110)
    assert len(r["day"]) == len(r["oil"]) == 110 - 18 + 1
    assert np.all(r["oil"] > 0) and np.all(r["oil_p10"] <= r["oil"] + 1e-9) and r["cum_p10"] < r["cum_oil"] < r["cum_p90"]


def test_well_scale():
    assert m2.well_scale([]) == 1.0
    assert m2.well_scale([(100, 120)] * 6) > 1.05 > 1.0


def test_arps_baseline_decline():
    t = np.arange(60.0)
    q = m2.arps(t, 80, 0.02, 0.5)
    assert abs(m2.arps_baseline(t, q, t)[30] - q[30]) / q[30] < 0.05


def test_shipped_m1_m2(shipped):
    a, b = shipped("M1"), shipped("M2")
    assert a["metrics"]["mae_T_ml"] <= 6 and a["metrics"]["mae_rh_ml"] <= 0.8
    assert a["metrics"]["mae_T_ml"] < a["metrics"]["mae_T_analytic"]
    assert b["primary"]["value"] <= 10 and b["primary"]["value"] < b["primary"]["baseline"]
    assert 0.75 <= b["metrics"]["cycle_cover80_mean"] <= 0.85
