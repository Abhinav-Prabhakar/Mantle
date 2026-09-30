from __future__ import annotations

import numpy as np
import pytest

from mantle_ml.models import m6_anomaly as m6


def test_runs_and_events():
    f = np.array([0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0], dtype=bool)
    assert m6.runs(f) == [(1, 3), (6, 6), (8, 11)]
    pred = m6.predicted_events(np.array([0, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0.0]), 1.0)
    assert pred == [(1, 3), (8, 11)]
    tp, fp, fn = m6.event_counts([(1, 3), (20, 25)], [(2, 4), (40, 50)])
    assert (tp, fp, fn) == (1, 1, 1)
    assert m6.f1_from(1, 1, 1) == pytest.approx(0.5)


def test_quantile_map_monotone():
    q = m6.Quantile(np.random.default_rng(0).exponential(1.0, 5000))
    v = np.array([0.1, 1.0, 5.0, 50.0])
    s = q(v)
    assert np.all(np.diff(s) > 0) and s[-1] > 1.0


def test_zscore_masks_nan():
    x = np.random.default_rng(1).normal(10, 1, (100, 3))
    x[:, 1] = np.nan
    z, mask, (med, sc) = m6.zscore(x, 30)
    assert z.shape == x.shape and not mask[:, 1].any() and np.isfinite(z).all()


def test_m6_quick_train_and_score(ml_data, quick_models):
    ev = m6.train(quick_models, quick=True)
    assert 0 <= ev["metrics"]["f1_s3_ens"] <= 1
    det = m6.AnomalyDetector.load(quick_models / "M6")
    rng = np.random.default_rng(0)
    x = np.column_stack([rng.normal(30, 0.5, 300), rng.normal(5, 0.2, 300), rng.normal(10, 0.1, 300), rng.normal(0.6, 0.01, 300),
                         rng.normal(0.3, 0.005, 300), rng.normal(45, 0.2, 300)])
    x[200:240, 3] *= 0.5            # THP collapse
    r = det.score_series(x, n_base=100)
    assert r["score"].shape == (300,) and np.isnan(r["score"][: m6.L - 1]).all()
    assert np.nanmean(r["score"][205:240]) > np.nanmean(r["score"][120:190])
    assert len(r["type"]) == 300


def test_shipped_m6(shipped):
    m = shipped("M6")["metrics"]
    assert m["f1_s3_ens"] >= m["f1_s3_3sigma"]
    if m.get("f1_3w_ens") is not None:
        assert m["f1_3w_ens"] > m["f1_3w_3sigma"]
