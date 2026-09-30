"""S3: 1 Hz SRP telemetry with sensor noise, drift, dropouts, spikes and labelled injected anomalies.

The mechanical signals come from the twin: one stroke of polished-rod load/position is stepped out of
``WellSim`` per 6-hour set-point segment and replayed at 1 Hz with a running phase. Motor amps/kW, VFD Hz and
the slow pressures/temperatures come from the same metrics plus ``mantle_physics.derive``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.signal import lfilter

from mantle_physics import WellSim, derive

from ..schemas import ANOMALY_LABELS
from .common import SEED, SOURCE, Scale, get_scale, rng_for

SEG_S = 6 * 3600
KD_CHOICES = np.array([0.46, 0.5, 0.54, 0.58, 0.62])
T0 = datetime(2026, 8, 1, 0, 0, 0)          # IST, naive
LABEL_IDX = {n: i for i, n in enumerate(ANOMALY_LABELS)}
EVENT_RATES = {"pump_off": 0.6, "gas_lock": 0.25, "load_cell_fault": 0.12, "tubing_leak_onset": 0.03,
               "vfd_trip": 0.2}
EVENT_DUR_S = {"pump_off": (1200, 5400), "gas_lock": (1800, 7200), "load_cell_fault": (600, 3600),
               "tubing_leak_onset": (6 * 3600, 48 * 3600), "vfd_trip": (300, 1800)}
MIN_ONE = ("pump_off", "gas_lock", "load_cell_fault", "vfd_trip")


@dataclass
class Waveform:
    period: float
    t: np.ndarray
    load: np.ndarray
    pos: np.ndarray
    metrics: object
    derived: dict


def stroke_waveform(spm: float, day: float, kd: float, steam: float, dt: float = 0.05) -> Waveform:
    sim = WellSim(spm=spm, cycle_day=day, kd=kd, steam=steam)
    m = sim.metrics()
    ts, load, pos = [0.0], [sim.state.load], [sim.state.rod_pos]
    th_prev, unwrapped, t = sim.theta, 0.0, 0.0
    for _ in range(int(3 * 60 / max(spm, 0.5) / dt) + 5):
        sim.step(dt)
        t += dt
        d = (sim.theta - th_prev) % (2 * np.pi)
        th_prev = sim.theta
        unwrapped += d
        ts.append(t)
        load.append(sim.state.load)
        pos.append(sim.state.rod_pos)
        if unwrapped >= 2 * np.pi:
            break
    # close the loop on the exact period (linear interpolation of the last step)
    over = unwrapped - 2 * np.pi
    period = t - (over / d) * dt if d > 0 else t
    ts_a, ld, ps = np.array(ts), np.array(load), np.array(pos)
    keep = ts_a < period
    ts_a, ld, ps = ts_a[keep], ld[keep], ps[keep]
    return Waveform(float(period), ts_a, ld, ps, m, derive(m, sim.state))


def _ou(rng: np.random.Generator, n: int, tau: float, sigma: float) -> np.ndarray:
    a = np.exp(-1.0 / tau)
    e = rng.standard_normal(n) * sigma * np.sqrt(1 - a * a)
    return lfilter([1.0], [1.0, -a], e)


def _place_events(rng: np.random.Generator, n: int, days: float) -> list[tuple[str, int, int]]:
    events: list[tuple[str, int, int]] = []
    for label, rate in EVENT_RATES.items():
        k = int(rng.poisson(rate * days))
        if label in MIN_ONE:
            k = max(k, 1)
        if label == "tubing_leak_onset":
            k = min(k, 1)
        lo, hi = EVENT_DUR_S[label]
        for _ in range(k):
            dur = int(rng.uniform(lo, hi))
            dur = min(dur, int(0.25 * n))
            for _try in range(60):
                s = int(rng.integers(0, max(1, n - dur - 1)))
                e = s + dur
                if all(e + 300 < s2 or s > e2 + 300 for _, s2, e2 in events):
                    events.append((label, s, e))
                    break
    return sorted(events, key=lambda x: x[1])


def generate_well(well: dict, days: int, seed: int = SEED, hz: float = 1.0, steam: float = 800.0,
                  start_day: float | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Telemetry for one well: returns (rows, injected-event table)."""
    wid = well["well_id"]
    rng = rng_for(seed, "S3", int(wid.split("-")[1]))
    n = int(days * 86400 * hz)
    d0 = float(start_day if start_day is not None else rng.uniform(22, max(23.0, 118 - days)))
    d0 = min(d0, 119.0 - days) if days < 96 else 22.0
    base_spm = float(rng.uniform(4.2, 6.8))
    eff_steam = float(np.clip(round(steam * well.get("steam_eff", 1.0)), 300, 1400))

    load = np.empty(n)
    pos = np.empty(n)
    amps = np.empty(n)
    hz_v = np.empty(n)
    thp = np.empty(n)
    chp = np.empty(n)
    flow = np.empty(n)
    pprl_arr = np.empty(n)
    spm_arr = np.empty(n)
    phase_off = float(rng.uniform(0, 10))
    spm_cur = base_spm
    n_seg = int(np.ceil(n / (SEG_S * hz)))
    for s in range(n_seg):
        i0, i1 = int(s * SEG_S * hz), min(n, int((s + 1) * SEG_S * hz))
        spm_cur = float(np.clip(spm_cur + rng.normal(0, 0.15), base_spm - 0.6, base_spm + 0.6))
        kd = float(rng.choice(KD_CHOICES))
        day = d0 + (i0 / hz) / 86400
        w = stroke_waveform(spm_cur, min(day, 120.0), kd, eff_steam)
        t = np.arange(i1 - i0) / hz + phase_off
        ph = t % w.period
        load[i0:i1] = np.interp(ph, w.t, w.load, period=w.period)
        pos[i0:i1] = np.interp(ph, w.t, w.pos, period=w.period)
        m, dv = w.metrics, w.derived
        pprl_arr[i0:i1] = m.pprl
        spm_arr[i0:i1] = spm_cur
        amps[i0:i1] = dv["ampsAvg"] * (0.55 + 0.9 * np.clip(load[i0:i1] / max(m.pprl, 1e-6), 0, 1.2))
        hz_v[i0:i1] = dv["hz"]
        thp[i0:i1] = dv["thp"]
        chp[i0:i1] = dv["chp"]
        flow[i0:i1] = dv["flowT"]
        phase_off = (phase_off + (i1 - i0) / hz) % w.period
    tsec = np.arange(n) / hz
    hour = tsec / 3600
    ambient = 30 + 8 * np.sin(2 * np.pi * (hour - 15) / 24)
    flow = flow + 0.06 * (ambient - 30)
    kw_scale = 1.732 * 415 * 0.86 / 1000

    # ---- injected anomalies (on the clean signals)
    events = _place_events(rng, n, days)
    label = np.zeros(n, dtype=np.int8)
    for name, s, e in events:
        sl = slice(s, e)
        label[sl] = LABEL_IDX[name]
        m_load = float(load[sl].mean())
        pk = float(pprl_arr[s])
        if name == "pump_off":
            load[sl] = m_load + (load[sl] - m_load) * 0.55
            ph_k = (tsec[sl] * spm_arr[sl] / 60.0) % 1.0
            load[sl] -= 0.22 * pk * np.exp(-0.5 * ((ph_k - 0.62) / 0.03) ** 2)      # fluid-pound impact
            amps[sl] *= 0.8
            thp[sl] *= 0.88
        elif name == "gas_lock":
            wob = _ou(rng, e - s, 30, 0.03 * pk)
            load[sl] = m_load + (load[sl] - m_load) * 0.22 + wob
            amps[sl] *= 0.7
            thp[sl] *= 0.6
        elif name == "load_cell_fault":
            mode = int(rng.integers(0, 3))
            if mode == 0:
                load[sl] = load[s]
            elif mode == 1:
                load[sl] = 0.0
            else:
                load[sl] = np.clip(m_load + rng.standard_normal(e - s) * 0.5 * pk, 0, 2.5 * pk)
        elif name == "tubing_leak_onset":
            r = np.linspace(0, 0.4, e - s)
            load[sl] = m_load + (load[sl] - m_load) * (1 - r)
            thp[sl] *= 1 - 0.3 * r
            amps[sl] *= 1 - 0.1 * r
        elif name == "vfd_trip":
            hz_v[sl] = 0.0
            amps[sl] = 0.0
            load[sl] = m_load
            pos[sl] = pos[s]
    # ---- sensor imperfections
    sig_load = 0.0025 * pprl_arr
    drift = rng.uniform(-0.5, 0.5) * tsec / max(tsec[-1], 1) + 0.05 * np.sin(2 * np.pi * hour / 24)
    load_m = load + drift + rng.standard_normal(n) * sig_load
    is_fault = label == LABEL_IDX["load_cell_fault"]
    load_m[is_fault] = load[is_fault]
    spikes = rng.random(n) < (1.0 / 3600) / hz
    load_m[spikes] += rng.choice([-1, 1], spikes.sum()) * rng.uniform(0.15, 0.4, spikes.sum()) * pprl_arr[spikes]
    pos_m = pos + rng.standard_normal(n) * 0.0004
    amps_m = np.maximum(0, amps * (1 + rng.standard_normal(n) * 0.008)) * (hz_v > 0)
    kw_m = amps_m * kw_scale * (1 + rng.standard_normal(n) * 0.01)
    hz_m = np.maximum(0, hz_v + rng.standard_normal(n) * 0.02) * (hz_v > 0)
    thp_m = thp + _ou(rng, n, 600, 0.015) + 0.01 * np.sin(2 * np.pi * hour / 24)
    chp_m = chp + _ou(rng, n, 900, 0.008)
    flow_m = flow + _ou(rng, n, 1200, 0.3)
    df = pd.DataFrame({
        "ts": pd.to_datetime(T0) + pd.to_timedelta(np.round(tsec * 1000).astype("int64"), unit="ms"),
        "well_id": wid,
        "load_kn": np.round(load_m, 2).astype("float32"),
        "pos_m": np.round(pos_m, 3).astype("float32"),
        "amps": np.round(amps_m, 1).astype("float32"),
        "kw": np.round(kw_m, 2).astype("float32"),
        "vfd_hz": np.round(hz_m, 2).astype("float32"),
        "thp_mpa": np.round(thp_m, 2).astype("float32"),
        "chp_mpa": np.round(chp_m, 2).astype("float32"),
        "flowline_t_c": np.round(flow_m, 1).astype("float32"),
        "label": pd.Categorical.from_codes(label, list(ANOMALY_LABELS)),
        "source": SOURCE,
    })
    df["ts"] = df["ts"].astype("datetime64[ms]")
    # dropouts: whole-row gaps (NaN measurements, label kept)
    n_drop = int(rng.poisson(2.0 * days))
    for _ in range(n_drop):
        s = int(rng.integers(0, n))
        e = min(n, s + int(rng.uniform(3, 120) * hz))
        for c in ("load_kn", "pos_m", "amps", "kw", "vfd_hz", "thp_mpa", "chp_mpa", "flowline_t_c"):
            df.iloc[s:e, df.columns.get_loc(c)] = np.nan
    ev = pd.DataFrame([{
        "well_id": wid, "label": name,
        "start_ts": pd.Timestamp(T0) + pd.Timedelta(seconds=s / hz),
        "end_ts": pd.Timestamp(T0) + pd.Timedelta(seconds=e / hz),
        "duration_s": float((e - s) / hz), "source": SOURCE,
    } for name, s, e in events])
    if ev.empty:
        ev = pd.DataFrame(columns=["well_id", "label", "start_ts", "end_ts", "duration_s", "source"])
    return df, ev


def generate(wells: pd.DataFrame, cycles: pd.DataFrame | None, scale: str | Scale = "default",
             seed: int = SEED, out_dir=None) -> pd.DataFrame:
    """Generate telemetry for the first ``tele_wells`` wells (showcase first); writes
    ``out_dir/telemetry/well_id=<id>/part-0.parquet`` if ``out_dir`` and returns the event table."""
    from .common import SHOWCASE_ID

    sc = get_scale(scale)
    ids = [SHOWCASE_ID] + [w for w in wells["well_id"] if w != SHOWCASE_ID]
    ids = ids[: sc.tele_wells]
    evs = []
    for wid in ids:
        well = wells[wells.well_id == wid].iloc[0].to_dict()
        steam = 800.0
        if cycles is not None and (cycles.well_id == wid).any():
            steam = float(cycles[cycles.well_id == wid].iloc[-1]["steam_t"])
        df, ev = generate_well(well, sc.tele_days, seed, sc.tele_hz, steam)
        if out_dir is not None:
            p = out_dir / "telemetry" / f"well_id={wid}"
            p.mkdir(parents=True, exist_ok=True)
            df.drop(columns=["well_id"]).to_parquet(p / "part-0.parquet", index=False, compression="zstd",
                                                     row_group_size=1_000_000)
        evs.append(ev)
        if out_dir is None:
            evs[-1].attrs["frame"] = df
    return pd.concat(evs, ignore_index=True)
