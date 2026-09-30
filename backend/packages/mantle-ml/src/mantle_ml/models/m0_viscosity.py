"""M0 viscosity: Walther/ASTM D341 per-well fit + monotone LightGBM residual (decreasing in T).

Honesty note: real sample-level literature data was unavailable (``data/reference/viscosity_literature.csv``
holds column statistics only). Training data are physics-synthetic well fluids: lab-like points from the twin's
Walther law with per-well multipliers, an asphaltene/resin/WAT structural deviation that Walther cannot express
(decreasing in T), and lognormal measurement noise. The literature envelope is used only as a range check.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from mantle_physics.viscosity import WAL_A, WAL_B

from .. import common

ID = "M0"
T_GRID = np.arange(20.0, 161.0, 10.0)
CAL_T = (50.0, 150.0)
FEATS = ["T", "api", "asph", "resin", "wat", "wA", "wB"]


def walther_fit(t1: float, mu1: float, t2: float, mu2: float) -> tuple[float, float]:
    def f(cp, c):
        return math.log10(math.log10(cp / 0.96 + 0.7)), math.log10(c + 273.15)

    y1, x1 = f(mu1, t1)
    y2, x2 = f(mu2, t2)
    B = (y1 - y2) / (x2 - x1)
    return y1 + B * x1, B


def walther(T, A, B):
    T = np.asarray(T, dtype=float)
    return (10 ** (10 ** (A - B * np.log10(T + 273.15))) - 0.7) * 0.96


def beggs_robinson(T_c, api):
    """Dead-oil viscosity (cP), Beggs-Robinson 1975 (a common correlation, poor for heavy oil)."""
    T_f = np.asarray(T_c, dtype=float) * 1.8 + 32
    x = 10 ** (3.0324 - 0.02023 * np.asarray(api, dtype=float)) * T_f ** -1.163
    return 10**x - 1


def _true_log10_mu(T, A, B, api, asph, resin, wat):
    base = np.log10(walther(T, A, B))
    dev = (0.10 * (asph / 9.5) * np.exp(-(T - 20) / 70) + 0.03 * (resin - 12) / 4 * np.exp(-(T - 20) / 50)
           + 0.08 / (1 + np.exp((T - (wat + 15)) / 8)))
    return base + dev


def make_fluids(n: int, seed: int = common.SEED) -> pd.DataFrame:
    r = np.random.default_rng([seed, 0])
    api = r.uniform(17, 19.5, n)
    asph = r.uniform(7, 12, n)
    resin = r.uniform(8, 16, n)
    wat = r.uniform(30, 50, n)
    vf = np.exp(r.normal(0, 0.15, n))
    rows = []
    for i in range(n):
        nu = WAL_A  # shift intercept so 50C viscosity scales by vf (same construction as S1)
        base50 = float(walther(50.0, WAL_A, WAL_B)) / 0.96
        lo, hi = math.log10(math.log10(base50 + 0.7)), math.log10(math.log10(base50 * vf[i] + 0.7))
        A = nu + (hi - lo)
        # API shifts the whole curve mildly (lighter = thinner)
        A += 0.004 * (18.2 - api[i])
        mu = 10 ** _true_log10_mu(T_GRID, A, WAL_B, api[i], asph[i], resin[i], wat[i])
        mu = mu * np.exp(r.normal(0, 0.04, len(T_GRID)))
        rows.append(pd.DataFrame({"fluid": i, "T": T_GRID, "api": api[i], "asph": asph[i], "resin": resin[i],
                                  "wat": wat[i], "mu": mu}))
    df = pd.concat(rows, ignore_index=True)
    ab = []
    for _, g in df.groupby("fluid"):
        m1 = g.loc[g["T"] == CAL_T[0], "mu"].iloc[0]
        m2 = g.loc[g["T"] == CAL_T[1], "mu"].iloc[0]
        ab.append((g["fluid"].iloc[0], *walther_fit(CAL_T[0], m1, CAL_T[1], m2)))
    ab = pd.DataFrame(ab, columns=["fluid", "wA", "wB"])
    df = df.merge(ab, on="fluid")
    df["mu_w"] = walther(df["T"], df["wA"], df["wB"])
    df["resid"] = np.log10(df["mu"] / df["mu_w"])
    return df


def _mape(y, p):
    return float(np.mean(np.abs(p - y) / y) * 100)


def _fit(df: pd.DataFrame, n_trees: int) -> lgb.Booster:
    mono = [-1 if f == "T" else 0 for f in FEATS]
    params = dict(objective="l2", learning_rate=0.08, num_leaves=8, min_data_in_leaf=20, monotone_constraints=mono,
                  monotone_constraints_method="advanced", verbose=-1, seed=common.SEED, feature_fraction=1.0)
    return lgb.train(params, lgb.Dataset(df[FEATS], df["resid"]), num_boost_round=n_trees)


def envelope_check(model: ViscosityModel) -> dict:
    """Range check against the literature envelope (column statistics): mu at >=50 C stays inside it x margin."""
    from mantle_data.paths import reference_dir

    p = reference_dir() / "viscosity_literature.csv"
    if not p.exists():
        return {"available": False}
    lit = pd.read_csv(p)
    lo, hi = float(lit["viscosity_cp"].min()), float(lit["viscosity_cp"].max())
    T = np.array([80.0, 120.0, 160.0])
    mu = np.array([float(model.predict(t, 18.0, 9.0)["mu_cp"]) for t in T])
    return {"available": True, "lit_min_cp": lo, "lit_max_cp": hi, "pred_80_120_160C": mu.tolist(),
            "inside": bool(np.all((mu > lo * 0.3) & (mu < hi * 5)))}


class ViscosityModel:
    def __init__(self, booster: lgb.Booster, meta: dict):
        self.booster, self.meta = booster, meta

    @classmethod
    def load(cls, d: Path) -> ViscosityModel:
        d = Path(d)
        return cls(joblib.load(d / "model.joblib"), json.loads((d / "meta.json").read_text()))

    def predict(self, T, api: float = 18.0, asph: float = 9.2, resin: float = 12.0, wat: float = 40.0,
                walther_ab: tuple[float, float] | None = None,
                points: tuple[tuple[float, float], tuple[float, float]] | None = None) -> dict:
        """mu (cP) at T (scalar or array). Walther params from ``points`` ((T1,mu1),(T2,mu2)), ``walther_ab``
        (e.g. the well table's walther_A/B) or the field default."""
        if points is not None:
            A, B = walther_fit(points[0][0], points[0][1], points[1][0], points[1][1])
        elif walther_ab is not None:
            A, B = walther_ab
        else:
            A, B = WAL_A, WAL_B
        Ta = np.atleast_1d(np.asarray(T, dtype=float))
        X = pd.DataFrame({"T": Ta, "api": api, "asph": asph, "resin": resin, "wat": wat, "wA": A, "wB": B})
        mw = walther(Ta, A, B)
        mu = mw * 10 ** self.booster.predict(X[FEATS])
        scalar = np.ndim(T) == 0
        return {"mu_cp": float(mu[0]) if scalar else mu, "mu_walther_cp": float(mw[0]) if scalar else mw,
                "model": ID, "version": self.meta["version"], "source": self.meta["source"]}


def train(out_dir: Path, quick: bool = False) -> dict:
    with common.timer() as tm:
        n = 40 if quick else 400
        df = make_fluids(n)
        folds = 3 if quick else 5
        trees = 40 if quick else 250
        oof = np.zeros(len(df))
        for tr, te in GroupKFold(folds).split(df, groups=df["fluid"]):
            b = _fit(df.iloc[tr], trees)
            oof[te] = b.predict(df.iloc[te][FEATS])
        mu_gbm = df["mu_w"].to_numpy() * 10**oof
        mu_br = beggs_robinson(df["T"], df["api"])
        m_hot = df["T"] >= 50
        met = {
            "mape_gbm_pct": _mape(df["mu"], mu_gbm), "mape_walther_2pt_pct": _mape(df["mu"], df["mu_w"]),
            "mape_beggs_robinson_pct": _mape(df["mu"], np.maximum(mu_br, 0.3)),
            "mape_gbm_ge50C_pct": _mape(df["mu"][m_hot], mu_gbm[m_hot]),
            "mape_walther_ge50C_pct": _mape(df["mu"][m_hot], df["mu_w"][m_hot]),
        }
        booster = _fit(df, trees)
    d = common.model_dir(ID, out_dir)
    joblib.dump(booster, d / "model.joblib", compress=3)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "features": FEATS,
            "trained_at": common.now_iso(), "n_fluids": n, "data_hash": common.data_hash([df])}
    (d / "meta.json").write_text(json.dumps(meta))
    model = ViscosityModel(booster, meta)
    T = np.arange(20.0, 160.0, 2.0)
    mono = all(np.all(np.diff(model.predict(T, a, s, 12, 40)["mu_cp"]) < 0) for a in (17, 18, 19.5) for s in (7, 9.5, 12))
    ev = {"metrics": met, "primary": {"name": "mape_gbm_ge50C_pct", "value": met["mape_gbm_ge50C_pct"], "target": 12.0,
                                     "baseline_name": "beggs_robinson", "baseline": met["mape_beggs_robinson_pct"],
                                     "direction": "lower"},
          "monotone_in_T": mono, "envelope": envelope_check(model), "train_seconds": tm["seconds"],
          "source": "physics_synthetic", "version": meta["version"], "data_hash": meta["data_hash"],
          "n_rows": len(df), "quick": quick}
    card = f"""# M0 viscosity (Walther + monotone LightGBM residual)
**Source of training data: physics_synthetic** (NOT real lab data). Real sample-level literature data was unavailable
(the reference CSV has column statistics only), so wells' lab-like points come from the twin's Walther law with
per-well multipliers, an asphaltene/resin/WAT deviation (decreasing in T) that Walther cannot express, and 4 %
lognormal noise. The GBM therefore learns *the generator's* deviation; the MAPE below is not evidence about real crude.

- Features: {", ".join(FEATS)} (wA/wB from a 2-point fit at 50/150 C). Target: log10(mu/mu_walther); LightGBM with monotone
  constraint decreasing in T, so the total curve is strictly decreasing.
- Metrics (5-fold, grouped by fluid): {json.dumps(ev["metrics"])}
- Baselines: Beggs-Robinson dead oil ({met["mape_beggs_robinson_pct"]:.0f} % MAPE: it is not built for 12,000 cP oils), plain 2-point Walther.
- Envelope check vs literature statistics: {json.dumps(ev["envelope"])}
- Limits: inference at temperatures outside 20-160 C or API outside 17-19.5 extrapolates; no pressure/gas effects.
"""
    return common.write_eval(d, ID, ev, card)
