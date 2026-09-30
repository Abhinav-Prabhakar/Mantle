"""M1 thermal surrogate: sandface T(t), heated radius r_h(t) and thermal battery per cycle day.

Analytic baseline: the twin's Marx-Langenheim/Boberg-Lantz thermal law evaluated at the nominal steam volume and the
actual cycle day. LightGBM learns the residual (quantiles 0.1/0.5/0.9) from physics features; group k-fold by well.
Data are S2 daily rows (physics_synthetic).
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd

from mantle_physics.constants import T_RES

from .. import common, data, features

ID = "M1"
OUTS = {"T": "sandface_t_c", "rh": "heated_radius_m", "battery": "battery"}
BASE = {"T": "an_T", "rh": "an_rh", "battery": None}
QS = (0.1, 0.5, 0.9)
FEATS = ["steam_t", "inj_pressure_mpa", "steam_quality", "soak_days", "cycle_no", "steam_eff", "day", "phase_i",
         "dprod", "an_T", "an_rh", "an_exc", "an_Te", "an_rhe", "an_exce"]


def _base(df: pd.DataFrame, out: str) -> np.ndarray:
    if out == "battery":
        return np.clip(df["an_exc"] / df.groupby(["well_id", "cycle_no"])["an_exc"].transform("max").clip(lower=1e-6), 0, 1).to_numpy()
    return df[BASE[out]].to_numpy()


def _params(q: float | None, trees: int) -> dict:
    p: dict = {"learning_rate": 0.08, "num_leaves": 15, "min_data_in_leaf": 30, "verbose": -1, "seed": common.SEED,
         "n_jobs": 4, "feature_fraction": 0.9}
    p.update({"objective": "quantile", "alpha": q} if q is not None else {"objective": "l2"})
    return p | {"_trees": trees}


def _fit(df: pd.DataFrame, out: str, q: float, trees: int) -> lgb.Booster:
    p = _params(q, trees)
    n = p.pop("_trees")
    y = df[OUTS[out]].to_numpy() - _base(df, out)
    return lgb.train(p, lgb.Dataset(df[FEATS], y), num_boost_round=n)


class ThermalModel:
    def __init__(self, models: dict[str, dict[float, lgb.Booster]], meta: dict):
        self.models, self.meta = models, meta

    @classmethod
    def load(cls, d: Path) -> ThermalModel:
        d = Path(d)
        return cls(joblib.load(d / "model.joblib"), json.loads((d / "meta.json").read_text()))

    def frame(self, steam_t, days, p_inj=9.0, quality=0.72, soak_d=4.0, cycle_no=1, steam_eff=1.0) -> pd.DataFrame:
        d = np.atleast_1d(np.asarray(days, dtype=float))
        n = len(d)
        a_p = 14 + soak_d
        T, rh, ex = features.analytic_thermal(np.full(n, steam_t), d)
        Te, rhe, exe = features.analytic_thermal(np.full(n, steam_t), d, np.full(n, steam_eff))
        return pd.DataFrame({
            "steam_t": steam_t, "inj_pressure_mpa": p_inj, "steam_quality": quality, "soak_days": soak_d,
            "cycle_no": cycle_no, "steam_eff": steam_eff, "day": d,
            "phase_i": np.where(d < 14, 0, np.where(d < a_p, 1, 2)), "dprod": d - a_p,
            "an_T": T, "an_rh": rh, "an_exc": ex, "an_Te": Te, "an_rhe": rhe, "an_exce": exe,
        })

    def predict(self, steam_t: float, days, p_inj: float = 9.0, quality: float = 0.72, soak_d: float = 4.0,
                cycle_no: int = 1, steam_eff: float = 1.0, quantiles: bool = True) -> dict:
        """Arrays over ``days`` for T (C), r_h (m), battery (0..1); ``*_p10/_p90`` when ``quantiles``."""
        f = self.frame(steam_t, days, p_inj, quality, soak_d, cycle_no, steam_eff)
        res: dict = {"day": f["day"].to_numpy()}
        for out in OUTS:
            base = _base_frame(f, out)
            lo, hi = (OUT_LIMITS[out])
            for q, name in ((0.5, out), (0.1, f"{out}_p10"), (0.9, f"{out}_p90")):
                if q != 0.5 and not quantiles:
                    continue
                v = base + self.models[out][q].predict(f[FEATS])
                res[name] = np.clip(v, lo, hi)
            if quantiles:
                a, b = np.minimum(res[f"{out}_p10"], res[out]), np.maximum(res[f"{out}_p90"], res[out])
                res[f"{out}_p10"], res[f"{out}_p90"] = a, b
        res.update({"model": ID, "version": self.meta["version"], "source": self.meta["source"]})
        return res


OUT_LIMITS = {"T": (T_RES - 1, 400.0), "rh": (0.0, 30.0), "battery": (0.0, 1.0)}


def _base_frame(f: pd.DataFrame, out: str) -> np.ndarray:
    if out == "battery":
        return np.clip(f["an_exc"] / max(float(f["an_exc"].max()), 1e-6), 0, 1).to_numpy()
    return f[BASE[out]].to_numpy()


def oof_median_predictions(df: pd.DataFrame, folds: np.ndarray, trees: int) -> pd.DataFrame:
    """Out-of-fold median predictions (used by M2 so it never sees in-sample M1 outputs)."""
    out = pd.DataFrame(index=df.index, columns=list(OUTS), dtype=float)
    for k in np.unique(folds):
        tr, te = df[folds != k], df[folds == k]
        for o in OUTS:
            b = _fit(tr, o, 0.5, trees)
            out.loc[te.index, o] = _base(te, o) + b.predict(te[FEATS])
    return out


def _tables(quick: bool) -> pd.DataFrame:
    if quick:
        data.ensure_small_data()
    df = features.daily_table(data.cycles(), data.cycle_daily(), data.wells())
    return df


def train(out_dir: Path, quick: bool = False) -> dict:
    with common.timer() as tm:
        df = _tables(quick).reset_index(drop=True)
        if quick and len(df) > 6000:
            keep = df["well_id"].unique()[:12]
            df = df[df["well_id"].isin(keep)].reset_index(drop=True)
        n_splits = 2 if quick else 5
        trees = 30 if quick else 150
        folds = features.group_folds(df["well_id"], n_splits)
        oof = {o: {q: np.zeros(len(df)) for q in QS} for o in OUTS}
        for k in range(n_splits):
            tr, te = df[folds != k], df[folds == k]
            for o in OUTS:
                for q in QS:
                    if quick and q != 0.5 and o != "T":
                        oof[o][q][te.index] = np.nan
                        continue
                    oof[o][q][te.index] = _base(te, o) + _fit(tr, o, q, trees).predict(te[FEATS])
        met: dict = {}
        for o, col in OUTS.items():
            y = df[col].to_numpy()
            met[f"mae_{o}_ml"] = float(np.nanmean(np.abs(oof[o][0.5] - y)))
            met[f"mae_{o}_analytic"] = float(np.mean(np.abs(_base(df, o) - y)))
            if not (quick and o != "T"):
                lo, hi = oof[o][0.1], oof[o][0.9]
                met[f"cover80_{o}"] = float(np.mean((y >= np.minimum(lo, hi)) & (y <= np.maximum(lo, hi))))
        models = {o: {q: _fit(df, o, q, trees) for q in QS} for o in OUTS}
    d = common.model_dir(ID, out_dir)
    joblib.dump(models, d / "model.joblib", compress=3)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "features": FEATS,
            "trained_at": common.now_iso(), "n_rows": len(df), "data_hash": common.data_hash([df[FEATS]])}
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "mae_T_C", "value": met["mae_T_ml"], "target": 6.0,
                                     "baseline_name": "analytic", "baseline": met["mae_T_analytic"],
                                     "direction": "lower", "secondary": {"name": "mae_rh_m", "value": met["mae_rh_ml"],
                                                                        "target": 0.8, "baseline": met["mae_rh_analytic"]}},
          "targets": {"mae_T_C": 6.0, "mae_rh_m": 0.8}, "train_seconds": tm["seconds"], "source": "physics_synthetic",
          "version": meta["version"], "data_hash": meta["data_hash"], "n_rows": len(df), "quick": quick,
          "cv": f"{n_splits}-fold grouped by well"}
    card = f"""# M1 thermal surrogate
Predicts sandface T, heated radius r_h and thermal battery over the cycle with quantiles 0.1/0.5/0.9.
**Source: physics_synthetic** (S2 daily rows from the twin, {len(df)} rows). The surrogate reproduces the twin's thermal law
(which S2 applies with per-well steam efficiency and soak-length time remapping), so accuracy shows how well the physics-feature
GBM absorbs those effects, not agreement with a real reservoir.
- Baseline: analytic thermal law at nominal steam and actual day. Features: {", ".join(FEATS)} (analytic T/r_h/excess also at the well's effective steam).
- {ev["cv"]}. Metrics: {json.dumps(met)}. Targets: MAE T <= 6 C, r_h <= 0.8 m.
- Limits: S2 is noiseless, so the 0.1/0.9 quantiles are narrow (coverage is reported, not tuned); no real steam-injection data used.
"""
    return common.write_eval(d, ID, ev, card)
