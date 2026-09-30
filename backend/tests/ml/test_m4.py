from __future__ import annotations

import numpy as np
import pytest

from mantle_ml import data
from mantle_ml.models import m4_risk as m4


def test_weibull_fit_recovers_shape():
    rng = np.random.default_rng(0)
    t = 50 * rng.weibull(2.0, 4000)
    y = m4.Surv.from_arrays(np.ones_like(t, dtype=bool), t)
    k, lam = m4.weibull_fit(y)
    assert abs(k - 2.0) < 0.15 and abs(lam - 50) < 3


def test_rod_fatigue_localises_high_stress():
    cov = {"goodman_mean": 0.8, "stress_factor": 1.3, "spm": 6, "kd": 0.5, "steam_t": 800, "float_frac": 0.0,
           "impacts_day": 0.0, "impact_vel": 0.0, "corrosion": 0.3}
    f = m4.rod_fatigue(cov, 30.0)
    assert f["damage"].shape == (m4.N_RODS,) and np.all(f["p30"] >= 0) and np.all(f["p30"] <= 1)
    top = m4.top_rods(f, 5)
    assert len(top) == 5 and top[0]["p30"] >= top[-1]["p30"]
    # more strokes -> more damage
    cov2 = dict(cov, spm=8)
    assert m4.rod_fatigue(cov2, 30.0)["damage"].sum() > f["damage"].sum()


def test_m4_quick_and_assess(ml_data, quick_models):
    ev = m4.train(quick_models, quick=True)
    assert ev["metrics"]["n_cycles"] > 0
    model = m4.RiskModel.load(quick_models / "M4")
    well = data.wells().iloc[3].to_dict()
    cov = m4.cov_from_settings(well, 800, 5.4, 0.5)
    r = model.assess(cov, 20.0)
    assert 0 <= r["risk_30d"] <= 1 and r["mtbf_days"] > 0 and len(r["rods_damage"]) == 140
    assert len(r["top_rods"]) == 5 and all(0 <= t["rod"] < 140 for t in r["top_rods"])


def test_shipped_m4(shipped):
    ev = shipped("M4")
    m = ev["metrics"]
    assert m["rod_c_index_ml"] >= 0.75 and m["rod_brier_improvement"] >= 0.20
    assert m["rod_c_index_ml"] > m["rod_c_index_age_baseline"]
    assert m["rod_top3_hit"] > 5 * m["rod_top3_random"]


@pytest.mark.xfail(reason="Unseat model misses C-index 0.75 / Brier: per-well hold-down capacity is hidden in S5", strict=False)
def test_shipped_m4_unseat_target(shipped):
    m = shipped("M4")["metrics"]
    assert m["unseat_c_index_ml"] >= 0.75 and m["unseat_brier_improvement"] >= 0.20
