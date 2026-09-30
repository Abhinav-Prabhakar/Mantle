from __future__ import annotations

import numpy as np

from mantle_ml import data
from mantle_ml.models import o3_rl as o3


def test_env_episode_and_reward(ml_data):
    wl = data.wells().to_dict("records")
    env = o3.CssEnv(wl, seed=0)
    obs, _ = env.reset()
    assert obs.shape == (16,) and np.isfinite(obs).all()
    total, done, steps = 0.0, False, 0
    while not done:
        obs, r, done, _, _ = env.step(np.zeros(5, dtype=np.float32))
        total += r
        steps += 1
        assert np.isfinite(r)
    assert steps == 1 + o3.N_BLOCKS


def test_blocks_cover_production():
    b = o3.blocks(120)
    assert b[0][0] == 18 and b[-1][1] == 120 and len(b) == o3.N_BLOCKS
    assert all(b[i][1] + 1 == b[i + 1][0] for i in range(len(b) - 1))


def test_o1_beats_static_in_env(ml_data):
    w = data.wells().iloc[0].to_dict()
    r = o3.evaluate_strategies([w], [3], None)
    assert r["o1_only"]["net"] > r["static"]["net"] and r["o1_only"]["impacts"] < r["static"]["impacts"]


def test_o3_quick_train(ml_data, quick_models):
    ev = o3.train(quick_models, quick=True)
    assert ev["metrics"]["ppo_net"] is not None
    pol = o3.RlPolicy.load(quick_models / "O3")
    a = pol.act(data.wells().iloc[1].to_dict(), 2)
    assert len(a["pump_by_block"]) == 4 and 500 <= a["plan"]["steam"] <= 1200


def test_shipped_o3(shipped):
    m = shipped("O3")["metrics"]
    assert m["o1_only_net"] > m["static_net"] and m["ppo_net"] > m["static_net"]
