from __future__ import annotations

import dataclasses
import time

import pytest

W = "/api/wells/BGW-17/live"


def test_live_shape_and_cadence(client):
    with client.websocket_connect(W) as ws:
        first = ws.receive_json()
        t0 = time.perf_counter()
        msgs = [ws.receive_json() for _ in range(8)]
        dt = time.perf_counter() - t0
    keys = {"t", "theta", "rod_pos", "load", "amps", "hz", "spm_actual", "thp", "chp", "anomaly_score", "anomaly_label",
            "last_stroke"}
    assert keys <= set(first) and set(first["last_stroke"]) >= {"n", "pounded", "severity"}
    assert 0.20 <= dt / 8 <= 0.45                                # one message every 250 ms
    assert all(b["t"] > a["t"] for a, b in zip([first, *msgs], msgs, strict=False))
    assert 0 <= first["rod_pos"] <= 3.03 and first["load"] > 0 and first["spm_actual"] > 4
    assert first["anomaly_label"] is None and first["warming_up"] is True     # no label without a threshold crossing


def test_live_retarget_and_last_stroke(client):
    with client.websocket_connect(W) as ws:
        ws.receive_json()
        ws.send_json({"spm": 12.0, "kd": 0.6})
        strokes, last = set(), None
        for _ in range(60):
            last = ws.receive_json()
            strokes.add(last["last_stroke"]["n"])
            if len(strokes) >= 3:
                break
        assert last["params"]["spm"] == 12.0 and last["spm_actual"] > 8
        assert max(strokes) >= 2                                  # M5 ran on completed strokes (n increments)
        assert 0 <= last["last_stroke"]["severity"] <= 1
        ws.send_json({"day": 5})
        m = ws.receive_json()
        for _ in range(3):
            m = ws.receive_json()
        assert m["phase"] == "INJECTION" and m["hz"] < 8            # the drive winds down while steaming


def test_apply_retargets_live_stream(client):
    with client.websocket_connect(W) as ws:
        ws.receive_json()
        r = client.post("/api/wells/BGW-17/apply", json={"spm": 3.5, "kd": 0.55})
        assert r.status_code == 200
        for _ in range(6):
            m = ws.receive_json()
        assert m["params"]["spm"] == 3.5 and m["params"]["kd"] == 0.55


def test_live_unknown_well(client):
    import pytest
    from starlette.websockets import WebSocketDisconnect

    with pytest.raises(WebSocketDisconnect), client.websocket_connect("/api/wells/NOPE/live") as ws:
        ws.receive_json()


# ---------------------------------------------------------------- M6 on the live stream (false positives / injected faults)


@pytest.fixture
def fast_clock(engine):
    """Time injection: every live message advances the twin by 1 s of simulated time, sent as fast as the server can run."""
    old = engine.s
    engine.s = dataclasses.replace(old, live_period_s=0.0, live_sim_dt_s=1.0, live_seed=7)
    yield engine
    engine.s = old


def _collect(ws, n):
    return [ws.receive_json() for _ in range(n)]


def test_live_steady_normal_60s_has_no_labels(client, fast_clock):
    with client.websocket_connect(W) as ws:
        msgs = _collect(ws, 60)                                    # 60 s of simulated streaming
    assert msgs[-1]["t"] == pytest.approx(60.0, abs=1.5)
    assert all(m["anomaly_label"] is None for m in msgs)           # the old bug: "load_cell_fault" right after connect
    assert all(m["warming_up"] for m in msgs)                      # < 24 live bins in a minute
    assert all(0.0 <= m["anomaly_score"] < m["anomaly_threshold"] for m in msgs)


def test_live_long_normal_stays_below_threshold(engine):
    from mantle_api.live import WARMUP_BINS, LiveSession

    wd = engine.store.well("BGW-17")
    old = engine.s
    try:
        for seed in range(4):
            engine.s = dataclasses.replace(old, live_seed=seed)
            sess = LiveSession(engine, wd)
            scores, labels, warm = [], [], 0
            for _ in range(30 * 60 * 4):                            # 30 simulated minutes at 4 Hz
                m = sess.tick(0.25)
                warm += bool(m["warming_up"])
                labels.append(m["anomaly_label"])
                if not m["warming_up"]:
                    scores.append(m["anomaly_score"])
            assert sess.n_live > 2 * WARMUP_BINS and scores
            assert not any(labels) and max(scores) < engine.reg.m6.thr
    finally:
        engine.s = old


def test_live_no_labels_during_warmup_even_with_a_fault(engine):
    from mantle_api.live import WARMUP_BINS, LiveSession

    old = engine.s
    try:
        engine.s = dataclasses.replace(old, live_seed=11)
        sess = LiveSession(engine, engine.store.well("BGW-17"))
        sess.inject("load_cell_fault", 3600)
        for _ in range(3600 * 4):
            m = sess.tick(0.25)
            if sess.n_live < WARMUP_BINS:
                assert m["anomaly_label"] is None and m["warming_up"]
            elif not m["warming_up"]:
                break
        assert sess.n_live >= WARMUP_BINS
    finally:
        engine.s = old


@pytest.mark.parametrize("kind", ["load_cell_fault", "pump_off", "gas_lock", "vfd_trip"])
def test_live_injected_fault_is_labelled(client, fast_clock, kind):
    with client.websocket_connect(W) as ws:
        msgs = _collect(ws, 600)                                   # 10 simulated minutes of normal operation first
        assert not any(m["anomaly_label"] for m in msgs) and not msgs[-1]["warming_up"]
        ws.send_json({"inject": {"kind": kind, "duration_s": 1200}})
        after = _collect(ws, 480)
    labels = {m["anomaly_label"] for m in after} - {None}
    assert labels, f"no label after injecting {kind}"
    assert any(m["fault"] == kind for m in after)
    hit = next(m for m in after if m["anomaly_label"])
    assert hit["anomaly_score"] > hit["anomaly_threshold"]
    if kind == "load_cell_fault":
        assert "load_cell_fault" in labels and any(m["load"] == 0.0 for m in after)
