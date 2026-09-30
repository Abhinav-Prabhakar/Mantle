"""WS /api/wells/{id}/live: a server-side twin stepped in real time, with M5 per stroke and M6 over the stream."""

from __future__ import annotations

import asyncio
import contextlib
import math
import time
from typing import Any

import numpy as np
from fastapi import WebSocket, WebSocketDisconnect

from mantle_data.synth.s3_telemetry import stroke_waveform
from mantle_physics import WellSim, derive
from mantle_physics.constants import SPM_MAX, SPM_MIN

from .engine import Engine
from .store import WellData

SUBSTEP = 0.05
N_PREFILL = 48          # baseline bins learned when the stream (re)starts
WINDOW = 96             # rolling window of stroke bins scored by M6
# measurement noise of the physics-synthetic sensor model (same magnitudes as the S3 generator)
SIG = {"load": 0.0025, "amps": 0.008, "thp": 0.015, "chp": 0.008, "flow": 0.3}


class LiveSession:
    def __init__(self, engine: Engine, wd: WellData):
        self.e, self.wd = engine, wd
        d = engine.live_defaults(wd)
        self.p = dict(d)
        self.rng = np.random.default_rng(int(time.time()) & 0xFFFF)
        self.sim = self._make()
        self.t = 0.0
        self.n = 0
        self.samples: list[tuple[float, float, float]] = []      # (t, pos, load kN) of the current stroke
        self.amps_samples: list[float] = []
        self.bins: list[list[float]] = []
        self.base: Any = None
        self.last_stroke = {"n": 0, "pounded": False, "severity": 0.0}
        self.score, self.label = 0.0, "normal"
        self.pending: dict | None = None
        self.prev_theta = self.sim.theta
        self._prefill()

    def _make(self) -> WellSim:
        p = self.p
        return WellSim(spm=p["spm"], cycle_day=p["day"], kd=p["kd"], steam=self.e.eff_steam(self.wd.row, p["steam"]))

    def retarget(self, **kw: float) -> None:
        self.pending = {**(self.pending or {}), **kw}

    def _apply_pending(self) -> bool:
        if not self.pending:
            return False
        q, self.pending = self.pending, None
        for k, lo, hi in (("spm", SPM_MIN, SPM_MAX), ("kd", 0.4, 0.7), ("day", 0.0, 120.0), ("steam", 300.0, 1400.0)):
            if k in q and q[k] is not None and math.isfinite(float(q[k])):
                self.p[k] = float(min(max(float(q[k]), lo), hi))
        old = self.sim
        self.sim = self._make()
        self.sim._spm_act = old._spm_act                # the drive ramps to the new speed, it does not jump
        self.samples.clear()
        self.amps_samples.clear()
        self._prefill()
        return True

    # ---------------------------------------------------------------- anomaly window
    def _noisy(self, load_mean: float, load_std: float, amps: float, dv: dict, pprl: float) -> list[float]:
        r = self.rng
        return [load_mean + r.normal(0, SIG["load"] * pprl), max(load_std * (1 + r.normal(0, 0.02)), 0.0),
                max(amps * (1 + r.normal(0, SIG["amps"])), 0.0), dv["thp"] + r.normal(0, SIG["thp"]),
                dv["chp"] + r.normal(0, SIG["chp"]), dv["flowT"] + r.normal(0, SIG["flow"])]

    def _prefill(self) -> None:
        """Baseline for M6: N bins of the twin's steady stroke at the current settings + sensor noise."""
        self.bins, self.base = [], None
        if self.sim._phase != "PRODUCTION":
            return
        p = self.p
        w = stroke_waveform(p["spm"], p["day"], p["kd"], self.e.eff_steam(self.wd.row, p["steam"]))
        m, dv = w.metrics, w.derived
        amps = dv["ampsAvg"] * (0.55 + 0.9 * np.clip(w.load / max(m.pprl, 1e-6), 0, 1.2))
        for _ in range(N_PREFILL):
            self.bins.append(self._noisy(float(w.load.mean()), float(w.load.std()), float(amps.mean()), dv, m.pprl))
        with contextlib.suppress(Exception):
            r = self.e.reg.score_telemetry(np.array(self.bins), n_base=N_PREFILL)
            self.base = r["baseline"]

    def _score(self) -> None:
        if self.base is None or len(self.bins) < 24:
            return
        r = self.e.reg.score_telemetry(np.array(self.bins[-WINDOW:]), base=self.base)
        s = float(r["score"][-1])
        self.score = s if math.isfinite(s) else 0.0
        self.label = str(r["type"][-1]) if bool(r["flag"][-1]) else "normal"

    # ---------------------------------------------------------------- stroke completion
    def _finish_stroke(self) -> None:
        s = self.samples
        self.samples = []
        amps = self.amps_samples
        self.amps_samples = []
        if len(s) < 12 or self.sim._phase != "PRODUCTION":
            return
        t = np.array([x[0] for x in s])
        pos = np.array([x[1] for x in s])
        load = np.array([x[2] for x in s])
        tq = np.linspace(t[0], t[-1], 96, endpoint=False)
        pq, lq = np.interp(tq, t, pos), np.interp(tq, t, load) * 1000.0
        est = self.e.reg.estimate_stroke(pq, lq, max(self.sim._spm_act, 0.5))
        self.n += 1
        sev = float(np.clip((0.85 - est["fillage"]) / 0.35, 0, 1))
        self.last_stroke = {"n": self.n, "pounded": bool(est["fillage"] < 0.85), "severity": sev,
                            "fillage": float(est["fillage"])}
        m = self.sim.metrics()
        dv = derive(m, self.sim.state)
        self.bins.append(self._noisy(float(np.mean(load / 1000.0)), float(np.std(load / 1000.0)),
                                     float(np.mean(amps)) if amps else dv["ampsAvg"], dv, m.pprl))
        self.bins = self.bins[-WINDOW * 2:]
        self._score()

    # ---------------------------------------------------------------- one 250 ms tick
    def tick(self, dt: float) -> dict:
        self._apply_pending()
        steps = max(1, int(round(dt / SUBSTEP)))
        for _ in range(steps):
            self.sim.step(SUBSTEP)
            self.t += SUBSTEP
            st = self.sim.state
            if st.theta < self.prev_theta - math.pi:
                self._finish_stroke()
            self.prev_theta = st.theta
            if self.sim._phase == "PRODUCTION":
                m = self.sim.metrics()
                dv = derive(m, st)
                self.samples.append((self.t, st.rod_pos, st.load))
                self.amps_samples.append(dv["amps"])
        m = self.sim.metrics()
        st = self.sim.state
        dv = derive(m, st)
        return {
            "t": round(self.t, 3), "theta": st.theta, "rod_pos": st.rod_pos, "load": st.load, "amps": dv["amps"],
            "hz": dv["hz"], "spm_actual": st.spm_actual, "thp": dv["thp"], "chp": dv["chp"],
            "anomaly_score": self.score, "anomaly_label": self.label, "last_stroke": self.last_stroke,
            "phase": self.sim._phase, "params": dict(self.p), "source": "physics_synthetic", "model": "M6",
        }


async def serve(ws: WebSocket, engine: Engine, wd: WellData) -> None:
    await ws.accept()
    sess = await asyncio.to_thread(LiveSession, engine, wd)
    engine.live_sessions.setdefault(wd.well_id, set()).add(sess)
    period = engine.s.live_period_s

    async def reader() -> None:
        try:
            while True:
                msg = await ws.receive_json()
                if isinstance(msg, dict):
                    sess.retarget(**{k: msg[k] for k in ("spm", "kd", "day", "steam") if k in msg})
        except (WebSocketDisconnect, RuntimeError, ValueError):
            return

    rtask = asyncio.create_task(reader())
    try:
        nxt = time.perf_counter()
        while not rtask.done():
            nxt += period
            msg = await asyncio.to_thread(sess.tick, period)
            await ws.send_json(msg)
            await asyncio.sleep(max(0.0, nxt - time.perf_counter()))
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        rtask.cancel()
        engine.live_sessions.get(wd.well_id, set()).discard(sess)
