from __future__ import annotations

import numpy as np

from mantle_ml.models import m0_viscosity as m0


def test_quick_train_and_monotone(quick_models):
    ev = m0.train(quick_models, quick=True)
    assert ev["monotone_in_T"]
    model = m0.ViscosityModel.load(quick_models / "M0")
    T = np.linspace(20, 160, 60)
    mu = model.predict(T, 18.0, 9.0)["mu_cp"]
    assert np.all(np.diff(mu) < 0) and np.all(mu > 0)


def test_walther_two_point_exact():
    A, B = m0.walther_fit(50, 12000, 150, 80)
    assert abs(m0.walther(50, A, B) - 12000) < 1 and abs(m0.walther(150, A, B) - 80) < 0.1


def test_envelope_and_shipped_metrics(shipped):
    ev = shipped("M0")
    assert ev["envelope"].get("inside", True)
    p = ev["primary"]
    assert p["value"] <= p["target"]          # MAPE <= 12 % (on the physics-synthetic fluids)
    assert p["value"] < p["baseline"]         # beats Beggs-Robinson
    assert ev["source"] == "physics_synthetic"
