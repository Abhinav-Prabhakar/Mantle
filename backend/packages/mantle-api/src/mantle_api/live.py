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
WARMUP_BINS = 24        # live bins (M6 window length) before any label may be emitted after a (re)start
PERSIST_BINS = 3        # a label needs this many consecutive flagged bins (the model's own event definition, MIN_RUN)
FAULTS = ("pump_off", "gas_lock", "load_cell_fault", "vfd_trip")
# measurement noise of the physics-synthetic sensor model, structured as in the S3 generator: white 1 Hz noise on load and
# amps (relative to pprl / reading, averaged over the samples of a bin) and Ornstein-Uhlenbeck (sigma, tau in s) on the
# wellhead channels. White noise of the full baseline magnitude on THP/CHP/flow would look like a high-frequency fault to M6.
SIG = {"load": 0.0025, "amps": 0.008}
OU = {"thp": (0.015, 600.0), "chp": (0.008, 900.0), "flow": (0.3, 1200.0)}


class LiveSession:
    def __init__(self, engine: Engine, wd: WellData):
        self.e, self.wd = engine, wd
        d = engine.live_defaults(wd)
        self.p = dict(d)
        seed = engine.s.live_seed
        self.rng = np.random.default_rng((int(time.time()) & 0xFFFF) if seed is None else seed)
        self.fault: dict | None = None                            # injected sensor/process fault (demo / test hook)
        self.n_live = 0                                           # live (non-baseline) bins since the last (re)start
        self.sim = self._make()
        self.t = 0.0
        self.n = 0
        self.samples: list[tuple[float, float, float]] = []      # (t, pos, load kN) of the current stroke
        self.amps_samples: list[float] = []
        self.bins: list[list[float]] = []
        self.base: Any = None
        self.last_stroke = {"n": 0, "pounded": False, "severity": 0.0}
        self.score: float = 0.0
        self.label: str | None = None
        self.ou = dict.fromkeys(("thp", "chp", "flow"), 0.0)      # slow, autocorrelated wellhead-sensor noise (as in S3)
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
    def _ou(self, key: str, dt: float) -> float:
        sig, tau = OU[key]
        a = math.exp(-dt / tau)
        self.ou[key] = self.ou[key] * a + sig * math.sqrt(1 - a * a) * float(self.rng.normal())
        return self.ou[key]

    def _noisy(self, load_mean: float, load_std: float, amps: float, dv: dict, pprl: float, dt: float = 11.0) -> list[float]:
        """One M6 bin (one stroke of ``dt`` seconds) with the sensor noise of the S3 generator."""
        r = self.rng
        n = max(dt, 1.0)                                   # 1 Hz samples averaged in the bin
        return [load_mean + r.normal(0, SIG["load"] * pprl / math.sqrt(n)), max(load_std * (1 + r.normal(0, 0.02)), 0.0),
                max(amps * (1 + r.normal(0, SIG["amps"] / math.sqrt(n))), 0.0), dv["thp"] + self._ou("thp", dt),
                dv["chp"] + self._ou("chp", dt), dv["flowT"] + self._ou("flow", dt)]

    def _prefill(self) -> None:
        """Baseline for M6: N bins of the twin's steady stroke at the current settings + sensor noise."""
        self.bins, self.base = [], None
        self.n_live = 0
        self.score, self.label = 0.0, None
        if self.sim._phase != "PRODUCTION":
            return
        p = self.p
        w = stroke_waveform(p["spm"], p["day"], p["kd"], self.e.eff_steam(self.wd.row, p["steam"]))
        m, dv = w.metrics, w.derived
        amps = dv["ampsAvg"] * (0.55 + 0.9 * np.clip(w.load / max(m.pprl, 1e-6), 0, 1.2))
        dt = 60.0 / p["spm"]
        for _ in range(N_PREFILL):
            self.bins.append(self._noisy(float(w.load.mean()), float(w.load.std()), float(amps.mean()), dv, m.pprl, dt))
        with contextlib.suppress(Exception):
            r = self.e.reg.score_telemetry(np.array(self.bins), n_base=N_PREFILL)
            self.base = r["baseline"]

    def inject(self, kind: str | None, duration_s: float = 600.0) -> None:
        """Inject (or clear with ``None``) a fault into the streamed sensors, as the S3 generator does for its labelled events."""
        self.fault = None if kind not in FAULTS else {"kind": kind, "until": self.t + max(float(duration_s), 1.0)}

    def _faulted(self, b: list[float]) -> list[float]:
        """The bin as the faulty sensor / process would report it (same transforms as the S3 event generator)."""
        f = self.fault
        if f is None or self.t >= f["until"]:
            self.fault = None
            return b
        load_m, load_s, amps, thp, chp, flow = b
        if f["kind"] == "pump_off":
            load_s, amps, thp = load_s * 0.55, amps * 0.8, thp * 0.88
        elif f["kind"] == "gas_lock":
            load_s, amps, thp = load_s * 0.22, amps * 0.7, thp * 0.6
        elif f["kind"] == "load_cell_fault":
            load_m, load_s = 0.0, 0.0
        elif f["kind"] == "vfd_trip":                        # drive tripped: rods stand still at the mean load, no current
            load_s, amps = 0.0, 0.0
        return [load_m, load_s, amps, thp, chp, flow]

    def _score(self) -> None:
        """M6 on the rolling bins. The label is None unless the score exceeds the model's calibrated threshold for
        ``PERSIST_BINS`` consecutive bins, and never during the warm-up."""
        if self.base is None or len(self.bins) < WARMUP_BINS:
            return
        m6 = self.e.reg.m6
        r = self.e.reg.score_telemetry(np.array(self.bins[-WINDOW:]), base=self.base)
        s = float(r["score"][-1])
        self.score = s if math.isfinite(s) else 0.0
        flags = np.asarray(r["flag"], dtype=bool)
        hot = self.n_live >= WARMUP_BINS and len(flags) >= PERSIST_BINS and bool(flags[-PERSIST_BINS:].all()) and self.score > m6.thr
        typ = str(r["type"][-1])
        self.label = (typ if typ != "normal" else "unclassified_anomaly") if hot else None

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
        self.bins.append(self._faulted(self._noisy(float(np.mean(load)), float(np.std(load)),
                                                   float(np.mean(amps)) if amps else dv["ampsAvg"], dv, m.pprl,
                                                   float(t[-1] - t[0]))))
        self.n_live += 1
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
        faulty_cell = self.fault is not None and self.fault["kind"] == "load_cell_fault" and self.t < self.fault["until"]
        return {
            "t": round(self.t, 3), "theta": st.theta, "rod_pos": st.rod_pos, "load": 0.0 if faulty_cell else st.load,
            "amps": dv["amps"],
            "hz": dv["hz"], "spm_actual": st.spm_actual, "thp": dv["thp"], "chp": dv["chp"],
            "anomaly_score": self.score, "anomaly_label": self.label, "anomaly_threshold": self.e.reg.m6.thr,
            "warming_up": self.n_live < WARMUP_BINS, "fault": self.fault["kind"] if self.fault else None,
            "last_stroke": self.last_stroke,
            "phase": self.sim._phase, "params": dict(self.p), "source": "physics_synthetic", "model": "M6",
        }


async def serve(ws: WebSocket, engine: Engine, wd: WellData) -> None:
    await ws.accept()
    sess = await asyncio.to_thread(LiveSession, engine, wd)
    engine.live_sessions.setdefault(wd.well_id, set()).add(sess)
    period = engine.s.live_period_s            # wall-clock cadence
    sim_dt = engine.s.live_sim_dt_s            # simulated seconds advanced per message (0.25 = real time)

    async def reader() -> None:
        try:
            while True:
                msg = await ws.receive_json()
                if isinstance(msg, dict):
                    if "inject" in msg:
                        inj = msg["inject"]
                        sess.inject(inj.get("kind") if isinstance(inj, dict) else None,
                                    float(inj.get("duration_s", 600.0)) if isinstance(inj, dict) else 0.0)
                    sess.retarget(**{k: msg[k] for k in ("spm", "kd", "day", "steam") if k in msg})
        except (WebSocketDisconnect, RuntimeError, ValueError):
            return

    rtask = asyncio.create_task(reader())
    try:
        nxt = time.perf_counter()
        while not rtask.done():
            nxt += period
            msg = await asyncio.to_thread(sess.tick, sim_dt)
            await ws.send_json(msg)
            await asyncio.sleep(max(0.0, nxt - time.perf_counter()))
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        rtask.cancel()
        engine.live_sessions.get(wd.well_id, set()).discard(sess)
