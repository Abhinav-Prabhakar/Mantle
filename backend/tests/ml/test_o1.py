from __future__ import annotations

import time

import numpy as np

from mantle_ml import fasttwin as ft
from mantle_ml.models import o1_srp as o1
from mantle_physics.constants import SOAK_END
from mantle_physics.economics import cycle
from mantle_physics.pump import core
from mantle_physics.reservoir import prod_base
from mantle_physics.rods import kd_table


def test_fasttwin_parity_with_scalar_twin():
    for steam, day, spm, kd in [(800, 60, 5.4, 0.5), (950, 33, 3.3, 0.54), (620, 100, 7.0, 0.62), (1100, 25, 8.5, 0.44)]:
        c = core(prod_base(float(steam), float(day)), spm, kd_table(kd))
        bs = o1.base_state(steam, day, o1.DEFAULT_WELL)
        r = ft.core(bs["qIn"], bs["wc"], bs["c"], bs["c500"], bs["c800"], spm, kd)
        for a, b in [(c.oil, r["oil"]), (c.fill, r["fill"]), (c.motorKw, r["kw"]), (c.goodman, r["goodman"]), (c.marginRaw, r["margin_raw"])]:
            assert abs(a - float(b)) <= 0.02 * max(abs(a), 0.2), (steam, day, spm, kd, a, float(b))
    cy = cycle(800, 5.4, 0.5)
    fd = ft.cycle_days(800, 5.4, 0.5)
    assert np.allclose(fd["oil"][SOAK_END:], cy.oil[SOAK_END:], rtol=1e-3, atol=1e-3)


def test_o1_output_shape_and_constraints():
    ft.tables()
    r = o1.recommend(800, 41, 5.4, 0.5)
    for k in ("title", "detail", "spm", "kd", "hz", "deltas", "confidence"):
        assert k in r
    assert set(r["deltas"]) >= {"oil", "float", "energy", "impacts"}
    assert 0 < r["confidence"] <= 1
    assert r["hz"] == r["spm"] * 50 / 9


def test_o1_respects_constraints_50_random_states_and_latency():
    ft.tables()
    o1.recommend(800, 41, 5.4, 0.5)          # warm-up (loads tables)
    lat = []
    for s in o1.sample_states(50, seed=99):
        t = time.perf_counter()
        r = o1.recommend(s["steam"], s["cycle_day"], s["spm"], s["kd"], s["well"])
        lat.append(time.perf_counter() - t)
        assert r["feasible"], s
        c = r["constraints"]
        assert c["margin_raw"] >= 0.15 - 1e-6 and c["fill"] >= 0.8 - 1e-6 and c["goodman"] <= 0.9 + 1e-6 and c["torque"] <= 1.0 + 1e-6
        assert 0.8 <= r["spm"] <= 9.0 and 0.4 <= r["kd"] <= 0.7
        assert r["deltas"]["impacts"] <= 1e-6 or r["impacts_per_day"]["now"] < 1.0
    assert max(lat) < 0.2 and np.median(lat) < 0.05


def test_o1_holds_outside_production():
    r = o1.recommend(800, 5, 5.4, 0.5)
    assert r["title"].startswith("Hold") and r["deltas"]["oil"] == 0


def test_shipped_o1(shipped):
    m = shipped("O1")["metrics"]
    assert m["impacts_reduction_all_states"] >= 0.15 and m["oil_change_all_states"] >= -0.02
    assert m["recommended_infeasible_share"] <= 0.05 and m["latency_ms_p95"] < 200
