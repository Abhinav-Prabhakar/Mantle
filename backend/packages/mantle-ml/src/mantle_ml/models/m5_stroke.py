"""M5 VFD / impact estimator: fillage, impacts/day, impact velocity and motor amps from one stroke of load + position.

Physics features (pump-card area, downstroke load-drop position -> fillage estimate, steepest drop) feed a small
LightGBM calibration per target. Baseline: fixed-threshold rules on the same drop position. Training strokes are
generated from the twin (physics_synthetic): sampled operating state -> time-uniform polished-rod load/position
with sensor noise; truth = the twin's fillage, ``derive`` impact/amps formulas.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd

from mantle_physics.constants import TAU
from mantle_physics.pump import core, load_model, surface_point
from mantle_physics.reservoir import prod_base
from mantle_physics.rods import HK, KX, NK, interp, kd_table

from .. import common
from .m3_dyno import impact_index

ID = "M5"
N = 96
TARGETS = ["fillage", "impacts_day", "impact_vel", "amps"]
FEATS = ["spm", "ptp_load", "mean_load", "min_over_mean", "span", "area_kj", "up_mean", "dn_mean", "drop_x", "drop_kn",
         "drop_sev", "fill_phys", "up_dn_ratio", "load_std"]


def impacts_per_day(spm, fill):
    """Fluid-pound impacts/day (twin ``derive`` law): every stroke below 85 % fillage, scaled by pound severity."""
    return np.asarray(spm) * 1440 * np.clip((0.85 - np.asarray(fill)) / 0.35, 0, 1)


def impact_velocity(spm, fill):
    return (0.15 + (1 - np.asarray(fill)) * 1.3) * np.asarray(spm) / 5.4


def simulate_stroke(steam: float, day: float, spm: float, kd: float, rng: np.random.Generator | None = None,
                    n: int = N) -> dict:
    """One stroke from the twin, sampled uniformly in time (like a 4 Hz stream), plus ground-truth targets."""
    b = prod_base(float(steam), float(day))
    kt = kd_table(kd)
    c = core(b, spm, kt)
    lm = load_model(c, kt)
    omega = TAU * spm / 60
    th = np.arange(NK) * HK
    s = np.asarray(kt.s)
    dt = HK / (omega * s)
    t = np.concatenate([[0.0], np.cumsum(dt)])
    period = t[-1]
    tq = np.arange(n) / n * period
    th_q = np.interp(tq, t, np.append(th, TAU))
    pos = np.array([interp(KX, x) for x in th_q])
    load = np.array([surface_point(lm, kt, x, omega)[1] for x in th_q]) * 1000.0   # N
    if rng is not None:
        load = load + rng.standard_normal(n) * 0.004 * c.pprl * 1000
        pos = pos + rng.standard_normal(n) * 0.0005
    amps_avg = c.motorKw * 1000 / (1.732 * 415 * 0.86)
    frac = np.clip(load / 1000 / max(c.pprl, 1e-6), 0, 1.2)
    fill = float(c.fill)
    return {"pos": pos, "load": load, "spm": spm,
            "truth": {"fillage": fill, "impacts_day": float(impacts_per_day(spm, fill)),
                      "impact_vel": float(impact_velocity(spm, fill)), "amps": float(amps_avg * (0.55 + 0.9 * frac.mean()))}}


def stroke_features(pos, load, spm: float) -> dict[str, float]:
    pos, load = np.asarray(pos, dtype=float), np.asarray(load, dtype=float)
    n = len(pos)
    span = max(float(np.ptp(pos)), 1e-9)
    ptp = max(float(np.ptp(load)), 1.0)
    dp = np.roll(pos, -1) - pos
    up = dp > 0
    area = 0.5 * abs(float(np.sum(pos * np.roll(load, -1) - np.roll(pos, -1) * load)))
    up_mean = float(load[up].mean()) if up.any() else float(load.mean())
    dn_mean = float(load[~up].mean()) if (~up).any() else float(load.mean())
    imp = impact_index(pos, load)
    # fillage estimate: position (fraction of stroke, from the top) where the downstroke load falls through mid-level
    i1, i0 = int(np.argmax(pos)), int(np.argmin(pos))
    idx = (np.arange(i1, i1 + ((i0 - i1) % n) + 1)) % n
    seg, ps = load[idx], (pos[idx] - pos.min()) / span
    hi = float(np.mean(seg[: max(2, len(seg) // 8)]))
    lo = float(np.min(seg))
    mid = 0.5 * (hi + lo)
    below = np.flatnonzero(seg < mid)
    fill_phys = float(ps[below[0]]) if len(below) else 0.0
    return {"spm": float(spm), "ptp_load": ptp, "mean_load": float(load.mean()), "min_over_mean": float(load.min() / max(load.mean(), 1.0)),
            "span": span, "area_kj": area / 1000.0, "up_mean": up_mean, "dn_mean": dn_mean, "drop_x": imp["x_frac"],
            "drop_kn": imp["drop_kn"], "drop_sev": imp["severity"], "fill_phys": fill_phys,
            "up_dn_ratio": up_mean / max(dn_mean, 1.0), "load_std": float(load.std())}


def threshold_baseline(f: dict[str, float]) -> dict[str, float]:
    """Fixed-threshold rules on the raw drop position (what an operator alarm would do)."""
    x = f["fill_phys"]
    fill = 0.95 if x > 0.9 else 0.8 if x > 0.75 else 0.6 if x > 0.5 else 0.4
    pound = fill < 0.85
    return {"fillage": fill, "impacts_day": f["spm"] * 1440.0 if pound else 0.0, "impact_vel": 0.6 if pound else 0.15,
            "amps": 8.0}


def make_dataset(n: int, seed: int) -> pd.DataFrame:
    r = np.random.default_rng([common.SEED, seed])
    rows = []
    for _ in range(n):
        steam = r.uniform(500, 1200)
        day = float(r.integers(19, 121))
        spm = r.uniform(2.0, 9.0)
        kd = float(r.uniform(0.42, 0.68))
        s = simulate_stroke(steam, day, spm, kd, r)
        f = stroke_features(s["pos"], s["load"], spm)
        rows.append({**f, **{f"y_{k}": v for k, v in s["truth"].items()}, "steam": steam, "day": day})
    return pd.DataFrame(rows)


class StrokeEstimator:
    def __init__(self, boosters: dict[str, lgb.Booster], meta: dict):
        self.b, self.meta = boosters, meta

    @classmethod
    def load(cls, d: Path) -> StrokeEstimator:
        d = Path(d)
        return cls(joblib.load(d / "model.joblib"), json.loads((d / "meta.json").read_text()))

    def estimate(self, pos, load, spm: float) -> dict:
        f = stroke_features(pos, load, spm)
        X = pd.DataFrame([f])[FEATS]
        out: dict[str, Any] = {k: float(self.b[k].predict(X)[0]) for k in TARGETS}
        out["fillage"] = float(np.clip(out["fillage"], 0.0, 0.98))
        out["impacts_day"] = float(max(0.0, out["impacts_day"]))
        out["impact_vel"] = float(max(0.0, out["impact_vel"]))
        out["impact"] = impact_index(pos, load)
        out.update({"model": ID, "version": self.meta["version"], "source": self.meta["source"]})
        return out


def _fit(X: pd.DataFrame, y, trees: int) -> lgb.Booster:
    p = {"objective": "l2", "learning_rate": 0.06, "num_leaves": 15, "min_data_in_leaf": 15, "verbose": -1,
         "seed": common.SEED, "n_jobs": 4}
    return lgb.train(p, lgb.Dataset(X[FEATS], y), num_boost_round=trees)


def train(out_dir: Path, quick: bool = False) -> dict:
    with common.timer() as tm:
        ntr, nte, trees = (300, 100, 60) if quick else (5000, 1500, 300)
        tr, te = make_dataset(ntr, 1), make_dataset(nte, 2)
        boosters = {k: _fit(tr, tr[f"y_{k}"], trees) for k in TARGETS}
        pred = {k: boosters[k].predict(te[FEATS]) for k in TARGETS}
        base = pd.DataFrame([threshold_baseline(r) for r in te.to_dict("records")])
        met = {}
        for k in TARGETS:
            y = te[f"y_{k}"].to_numpy()
            scale = 100.0 if k == "fillage" else 1.0
            met[f"mae_{k}_ml"] = float(np.mean(np.abs(pred[k] - y)) * scale)
            met[f"mae_{k}_threshold"] = float(np.mean(np.abs(base[k].to_numpy() - y)) * scale)
        met["mae_fillage_phys_raw"] = float(np.mean(np.abs(te["fill_phys"] - te["y_fillage"])) * 100)
    d = common.model_dir(ID, out_dir)
    joblib.dump(boosters, d / "model.joblib", compress=3)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "features": FEATS,
            "trained_at": common.now_iso(), "n_train": ntr, "data_hash": common.data_hash([tr[FEATS]])}
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "mae_fillage_pts", "value": met["mae_fillage_ml"], "target": 4.0,
                                     "baseline_name": "fixed_thresholds", "baseline": met["mae_fillage_threshold"],
                                     "direction": "lower"},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"],
          "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# M5 VFD / impact estimator
From one stroke (96 time-uniform samples of polished-rod load + position, spm) predicts fillage, impacts/day, impact velocity and mean motor amps.
**Source: physics_synthetic** ({ntr} training strokes drawn from the twin across steam 500-1200 t, cycle days 19-120, spm 2-9, kd 0.42-0.68, with load/position noise; targets are the twin's own fillage and `derive` impact/amps laws).
- Physics features: card area, up/down mean loads, steepest downstroke drop (position, kN, severity), drop-position fillage estimate. LightGBM calibrates each target.
- Metrics (held-out {nte} strokes): {json.dumps(met)}
- Baseline: fixed thresholds on the drop position (fillage buckets, pound if < 85 %, constant amps).
- Note: at typical spm the twin's surface card is dominated by inertia/drag, so the raw drop-position estimate is a weak fillage estimator (`mae_fillage_phys_raw`); the GBM recovers fillage from card area and load levels.
- Limits: the twin sets the truth, so the model calibrates the estimator against the twin, not against measured pump-off events. The fixed 4 Hz-like stroke length assumed is 96 points.
"""
    return common.write_eval(d, ID, ev, card)

