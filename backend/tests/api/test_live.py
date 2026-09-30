from __future__ import annotations

import time

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
    assert first["anomaly_label"] == "normal"


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
