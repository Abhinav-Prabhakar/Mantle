from __future__ import annotations

import json

import numpy as np
import pytest

from mantle_ml import data, registry
from mantle_ml.train import ORDER, train


@pytest.fixture(scope="module")
def quick_registry(ml_data, tmp_path_factory):
    root = tmp_path_factory.mktemp("reg_models")
    train(ORDER, quick=True, root=root, log=lambda *_: None, in_process=False)
    return root


@pytest.mark.slow
def test_registry_loads_everything(quick_registry):
    reg = registry.Registry.load(quick_registry, strict=True)
    assert set(reg.loaded) == set(registry.ALL_IDS) and reg.models_loaded() == 10
    info = json.loads((quick_registry / "registry.json").read_text())["models"]
    for mid in registry.ALL_IDS:
        for k in ("id", "version", "trained_at", "data_hash", "metrics", "source"):
            assert k in info[mid]


@pytest.mark.slow
def test_registry_predict_api(quick_registry):
    reg = registry.Registry.load(quick_registry, strict=True)
    well = data.wells().iloc[1].to_dict()
    v = reg.predict_viscosity(60.0, 18.0, 9.0)
    assert v["mu_cp"] > 0 and v["model"] == "M0" and v["trained_on"] and v["version"]
    t = reg.predict_thermal(800, np.arange(0, 121))
    assert t["T"].shape == (121,) and t["model"] == "M1"
    c = reg.predict_cycle(well, 800, 4, 5.4, 0.5, 110)
    assert c["cum_oil"] > 0 and c["source"] == "physics_synthetic"
    rec = reg.recommend_pump(800, 41, 5.4, 0.5, well)
    assert rec["model"] == "O1" and "deltas" in rec
    risk = reg.assess_risk(well, 800, 5.4, 0.5, 30.0)
    assert 0 <= risk["risk_30d"] <= 1 and risk["model"] == "M4"
    plan = reg.plan_next_cycle(well, 2, budget_s=1.0)
    assert plan["model"] == "O2" and "mantle" in plan
    act = reg.rl_action(well, 2)
    assert len(act["pump_by_block"]) == 4
    cards = data.read_cards(3, seed=1)
    k = reg.classify_card(cards["surface_pos"][0], cards["surface_load"][0], float(cards["spm"][0]))
    assert k["model"] == "M3" and 0 < k["conf"] <= 1
    s = reg.estimate_stroke(cards["surface_pos"][0], cards["surface_load"][0], float(cards["spm"][0]))
    assert s["model"] == "M5"


def test_shipped_registry_matches_artifacts():
    from mantle_ml import common

    p = common.models_dir() / "registry.json"
    if not p.exists():
        pytest.skip("no shipped registry")
    reg = json.loads(p.read_text())["models"]
    assert set(reg) == set(registry.ALL_IDS)
    assert all(not v.get("quick") for v in reg.values())
