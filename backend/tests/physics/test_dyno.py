"""Wave-equation downhole card and dyno-class synthesiser tests."""

from __future__ import annotations

import time

import numpy as np
import pytest

from mantle_physics.dyno import (
    CLASS_INDEX,
    DYNO_CLASSES,
    RodString,
    card_features,
    downhole_card,
    sample_params,
    surface_card_from_downhole,
    synthesize_cards,
)


def rms_rel(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)) / (np.max(b) - np.min(b)))


def known_card(n=256, fo=9000.0, stroke=2.6, kd=0.55):
    """A smooth, physically shaped pump card (position/load over one stroke, uniform in time)."""
    tau = np.arange(n) / n
    up = tau < 1 - kd
    u, v = tau / (1 - kd), (tau - (1 - kd)) / kd
    s = np.where(up, 0.5 * (1 - np.cos(np.pi * np.clip(u, 0, 1))), 0.5 * (1 + np.cos(np.pi * np.clip(v, 0, 1))))
    ss = lambda x: np.clip(x, 0, 1) ** 2 * (3 - 2 * np.clip(x, 0, 1))  # noqa: E731
    load = np.where(up, ss(s / 0.25), ss((s - 0.75) / 0.25)) * fo
    return stroke * s, load


def test_uniform_rod_analytic_standing_wave():
    """A standing wave p = P cos(k(L-x)) cos(wt) has a known surface (p, F) pair; invert and recover the pump."""
    L, A, w = 1000.0, 5e-4, 40.0
    rods = RodString(np.array([L]), np.array([A]), np.array([w]))
    a = float(rods.wave_speed[0])
    EA = float(rods.ea[0])
    T, n, P = 10.0, 64, 0.8
    t = np.arange(n) * T / n
    om = 2 * np.pi / T
    k = om / a
    pos_s = P * np.cos(k * L) * np.cos(om * t)
    F_s = -EA * P * k * np.sin(k * L) * np.cos(om * t) + rods.air_weight() * 0.874
    pos, load = downhole_card(pos_s, F_s, T, rods, damping=0.0, n_harm=4)
    assert np.allclose(pos, P * np.cos(om * t) + P, atol=1e-9 * P + 1e-9)
    assert np.allclose(load, 0.0, atol=1e-6 * EA * P * k)
    # and forward again
    sp, sf = surface_card_from_downhole(pos, load, T, rods, damping=0.0, n_harm=4)
    assert np.allclose(sp, pos_s - pos_s.min(), atol=1e-9)
    assert np.allclose(sf, F_s, atol=1e-6 * EA * P * k)


@pytest.mark.parametrize("damping", [0.0, 0.1, 0.25])
@pytest.mark.parametrize("method", ["spectral", "fd"])
def test_roundtrip_recovers_known_card_within_2pct(damping, method):
    dh_pos, dh_load = known_card()
    rods = RodString.default()
    for period in (6.0, 12.0, 25.0):
        sp, sl = surface_card_from_downhole(dh_pos, dh_load, period, rods, damping, n_harm=24, method=method)
        rp, rl = downhole_card(sp, sl, period, rods, damping, n_harm=24, method=method)
        assert rms_rel(rl, dh_load) < 0.02
        assert rms_rel(rp, dh_pos - dh_pos.min()) < 0.02


def test_surface_card_shows_rod_dynamics():
    dh_pos, dh_load = known_card()
    sp, sl = surface_card_from_downhole(dh_pos, dh_load, 8.0, damping=0.1)
    assert sl.max() - sl.min() > 1.0 * (dh_load.max() - dh_load.min()) * 0.5
    assert abs(sl.mean() - (dh_load.mean() + RodString.default().air_weight() * 0.874)) < 1.0


def test_fd_matches_spectral():
    dh_pos, dh_load = known_card()
    a = surface_card_from_downhole(dh_pos, dh_load, 7.0, damping=0.15, method="spectral")
    b = surface_card_from_downhole(dh_pos, dh_load, 7.0, damping=0.15, method="fd", fd_dx=3.0)
    assert rms_rel(b[1], a[1]) < 0.005 and rms_rel(b[0], a[0]) < 0.005
    ia = downhole_card(*a, 7.0, damping=0.15)
    ib = downhole_card(*a, 7.0, damping=0.15, method="fd", fd_dx=3.0)
    assert rms_rel(ib[1], ia[1]) < 0.005
    with pytest.raises(ValueError):
        downhole_card(*a, 7.0, method="nope")
    with pytest.raises(ValueError):
        surface_card_from_downhole(*a, 7.0, method="nope")


def test_batch_shapes_and_per_card_period():
    b = synthesize_cards(24, np.random.default_rng(3))
    pos, load = downhole_card(b.surface_pos, b.surface_load, b.period_s, damping=b.params["damping"])
    assert pos.shape == b.surface_pos.shape == (24, 128)
    assert load.shape == b.surface_load.shape


def test_taper_matters():
    rods = RodString.default()
    uniform = RodString(np.array([rods.total_length]), rods.area[:1], rods.weight[:1])
    dh_pos, dh_load = known_card()
    a = surface_card_from_downhole(dh_pos, dh_load, 7.0, rods)
    b = surface_card_from_downhole(dh_pos, dh_load, 7.0, uniform)
    assert rms_rel(a[1], b[1]) > 0.01
    tr = rods.truncate(600.0)
    assert tr.total_length == pytest.approx(600.0) and len(tr.length) == 2
    assert rods.truncate(5000.0).total_length == pytest.approx(rods.total_length)


# ----------------------------------------------------------------- 12 synthesised classes


@pytest.fixture(scope="module")
def batch():
    return synthesize_cards(np.repeat(np.arange(12), 40), np.random.default_rng(11))


def feats(batch, cls, k=40):
    idx = np.flatnonzero(batch.labels == CLASS_INDEX[cls])[:k]
    return [
        card_features(batch.dh_pos[i], batch.dh_load[i], batch.params["fluid_load"][i], batch.params["stroke"][i])
        for i in idx
    ]


def rng_of(f, key):
    v = [x[key] for x in f]
    return min(v), max(v)


def test_twelve_classes_defined():
    assert len(DYNO_CLASSES) == 12 and len(set(DYNO_CLASSES)) == 12


def test_normal_card_is_parallelogram(batch):
    f = feats(batch, "normal")
    assert rng_of(f, "up_mid")[0] > 0.95
    assert rng_of(f, "dn_mid")[1] < 0.05
    assert rng_of(f, "drop_pos")[0] > 0.9                 # load leaves the rods at the top of the stroke
    assert rng_of(f, "stroke_ratio")[0] > 0.8


def test_fluid_pound_sharp_drop_mid_downstroke(batch):
    f = feats(batch, "fluid_pound")
    lo, hi = rng_of(f, "drop_pos")
    assert lo > 0.45 and hi < 0.9
    assert rng_of(f, "drop_width")[1] < 0.08              # sharp
    assert rng_of(f, "up_mid")[0] > 0.95


def test_pump_off_drops_early(batch):
    assert rng_of(feats(batch, "pump_off"), "drop_pos")[1] < 0.45


def test_gas_interference_gradual_transition(batch):
    f = feats(batch, "gas_interference")
    assert rng_of(f, "drop_width")[0] > 0.1               # rounded, not sharp
    assert rng_of(f, "drop_pos")[0] > 0.3 and rng_of(f, "drop_pos")[1] < 0.85


def test_rod_float_short_plunger_stroke(batch):
    assert rng_of(feats(batch, "rod_float"), "stroke_ratio")[1] < 0.8 * 0.97 + 1e-9


def test_tubing_leak_low_flat_load(batch):
    f = feats(batch, "tubing_leak")
    lo, hi = rng_of(f, "up_mid")
    assert lo > 0.25 and hi < 0.75
    assert rng_of(f, "up_slope")[0] > -0.05


def test_travelling_valve_leak_load_decays_on_upstroke(batch):
    assert rng_of(feats(batch, "travelling_valve_leak"), "up_slope")[1] < -0.1


def test_standing_valve_leak_load_builds_on_downstroke(batch):
    f = feats(batch, "standing_valve_leak")
    assert rng_of(f, "dn_slope")[0] > 0.1 and rng_of(f, "up_mid")[0] > 0.95


def test_unseated_pump_collapsed_card(batch):
    assert rng_of(feats(batch, "unseated_pump"), "load_range")[1] < 0.2


def test_parted_rods_stationary_pump_and_light_surface_load(batch):
    idx = np.flatnonzero(batch.labels == CLASS_INDEX["parted_rods"])
    assert np.all(batch.dh_pos[idx] == 0) and np.all(batch.dh_load[idx] == 0)
    full = RodString.default().air_weight() * 0.874
    assert np.all(batch.surface_load[idx].mean(axis=1) < 0.93 * full)
    normal = np.flatnonzero(batch.labels == CLASS_INDEX["normal"])
    assert np.all(batch.surface_load[normal].mean(axis=1) > full)
    f = feats(batch, "parted_rods")
    assert rng_of(f, "stroke_ratio") == (0.0, 0.0)


def test_plunger_sticking_is_rough(batch):
    normal_rough = np.median([x["roughness"] for x in feats(batch, "normal")])
    rough = [x["roughness"] for x in feats(batch, "plunger_sticking")]
    assert np.median(rough) > 2 * normal_rough


def test_excessive_friction_fat_card(batch):
    f = feats(batch, "excessive_friction")
    assert rng_of(f, "dn_mid")[1] < -0.1
    assert rng_of(f, "load_range")[0] > 1.25


def test_classes_are_mutually_separable_by_features(batch):
    """A crude nearest-centroid on the features (not the ML model) separates most classes."""
    keys = ["stroke_ratio", "load_range", "up_mid", "dn_mid", "up_slope", "dn_slope", "drop_pos", "drop_width", "roughness"]
    X, y = [], []
    for c in DYNO_CLASSES:
        for f in feats(batch, c):
            X.append([f[k] for k in keys])
            y.append(CLASS_INDEX[c])
    X, y = np.array(X), np.array(y)
    X = (X - X.mean(0)) / (X.std(0) + 1e-9)
    cents = np.array([X[y == i].mean(0) for i in range(12)])
    pred = np.argmin(((X[:, None, :] - cents[None]) ** 2).sum(-1), axis=1)
    assert (pred == y).mean() > 0.8


def test_synth_is_deterministic_and_finite():
    a = synthesize_cards(24, np.random.default_rng(5), noise=0.01)
    b = synthesize_cards(24, np.random.default_rng(5), noise=0.01)
    assert np.array_equal(a.surface_load, b.surface_load)
    for arr in (a.surface_pos, a.surface_load, a.dh_pos, a.dh_load):
        assert np.all(np.isfinite(arr))
    assert a.class_names[:2] == ["normal", "fluid_pound"]
    c = synthesize_cards(["normal", "parted_rods"], np.random.default_rng(1))
    assert c.labels.tolist() == [0, 9]
    p = sample_params(np.array([1, 4, 9]), np.random.default_rng(2))
    assert p["fillage"][0] < 0.9 and p["fillage"][1] < 0.5 and not np.isnan(p["parted_depth"][2])


def test_throughput_over_2k_cards_per_second():
    n = 4000
    rng = np.random.default_rng(0)
    t0 = time.perf_counter()
    b = synthesize_cards(n, rng)
    downhole_card(b.surface_pos, b.surface_load, b.period_s, damping=b.params["damping"])
    rate = n / (time.perf_counter() - t0)
    assert rate > 2000, f"{rate:.0f} cards/s"
