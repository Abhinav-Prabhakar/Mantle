"""M2 cycle production forecaster: physics prior (Boberg-Lantz rate) x LightGBM multiplicative residual.

Daily oil over the production period with P10/P50/P90 (CQR on the daily level; split-conformal on the cycle
cum-oil level) and a per-well Bayesian scaling from the well's own history. Baseline: Arps hyperbolic decline fitted
to the previous cycle. Group k-fold by well; M1 inputs are out-of-fold so nothing leaks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from mantle_physics.constants import SOAK_END

from .. import common, data, features
from .. import fasttwin as ft
from . import m0_viscosity as m0
from . import m1_thermal as m1

ID = "M2"
FEATS = ["dprod", "day", "steam_t", "soak_days", "spm", "kd", "cycle_no", "pi_factor", "visc_factor", "steam_eff",
         "decline_rate", "m1_T", "m1_rh", "m1_battery", "mu_cp", "prior_oil", "inj_pressure_mpa", "steam_quality"]
PRIOR_STRENGTH = 2.0


def prior_oil(steam_t, dprod, soak, steam_eff, pi):
    """Boberg-Lantz-style reservoir rate of the twin (steam response x heated-zone productivity x depletion)."""
    tw = SOAK_END + np.asarray(dprod, dtype=float)
    tw = np.clip(tw, SOAK_END, 120)
    i0 = np.clip(np.floor(tw).astype(int), 0, 119)
    f = tw - i0
    b = ft.base_at(ft.eff_steam(np.asarray(steam_t, dtype=float), np.asarray(steam_eff, dtype=float)))
    q = ft.base_field(b, "qIn")
    wc = ft.base_field(b, "wc")
    ar = np.arange(len(i0)) if b.ndim == 3 else None
    if ar is None:
        rate = (q[i0] * (1 - f) + q[i0 + 1] * f) * (1 - (wc[i0] * (1 - f) + wc[i0 + 1] * f))
    else:
        rate = (q[ar, i0] * (1 - f) + q[ar, i0 + 1] * f) * (1 - (wc[ar, i0] * (1 - f) + wc[ar, i0 + 1] * f))
    return rate * np.asarray(pi, dtype=float)


def _feature_frame(df: pd.DataFrame, m1_pred: pd.DataFrame, visc: m0.ViscosityModel) -> pd.DataFrame:
    X = df.copy()
    X["m1_T"], X["m1_rh"], X["m1_battery"] = m1_pred["T"].to_numpy(), m1_pred["rh"].to_numpy(), m1_pred["battery"].to_numpy()
    X["prior_oil"] = prior_oil(X["steam_t"], X["dprod"], X["soak_days"], X["steam_eff"], X["pi_factor"])
    mu = np.empty(len(X))
    for i, (_, g) in enumerate(X.groupby("well_id")):
        r = g.iloc[0]
        mu[X.index.get_indexer(g.index)] = viscosity_for(visc, g["m1_T"].to_numpy(), r)
        del i
    X["mu_cp"] = mu
    return X


def viscosity_for(visc: m0.ViscosityModel, T, well) -> np.ndarray:
    return np.asarray(visc.predict(T, float(well["api"]), float(well["asphaltene_wt_pct"]),
                                   walther_ab=(float(well["walther_A"]), float(well["walther_B"]))) ["mu_cp"])


def _fit(X: pd.DataFrame, y: np.ndarray, kind: str, trees: int) -> lgb.Booster:
    p: dict = {"learning_rate": 0.06, "num_leaves": 31, "min_data_in_leaf": 40, "verbose": -1, "seed": common.SEED,
         "n_jobs": 4, "feature_fraction": 0.9, "lambda_l2": 1.0}
    p.update({"objective": "l2"} if kind == "mean" else {"objective": "quantile", "alpha": float(kind)})
    return lgb.train(p, lgb.Dataset(X[FEATS], y), num_boost_round=trees)


def arps(t, qi, D, b):
    return qi / np.power(1 + b * D * t, 1 / b)


def arps_baseline(prev_t: np.ndarray, prev_q: np.ndarray, t_new: np.ndarray) -> np.ndarray:
    """Hyperbolic decline fitted to the previous cycle's production, extrapolated over the new cycle's days."""
    try:
        popt, _ = curve_fit(arps, prev_t, prev_q, p0=[prev_q.max(), 0.01, 0.5],
                            bounds=([0, 1e-5, 0.05], [prev_q.max() * 3, 1.0, 1.5]), maxfev=4000)
        return arps(t_new, *popt)
    except Exception:
        return np.full_like(t_new, prev_q.mean(), dtype=float)


class ForecastModel:
    def __init__(self, boosters: dict[str, lgb.Booster], meta: dict, m1_model: m1.ThermalModel, visc: m0.ViscosityModel):
        self.b, self.meta, self.m1, self.visc = boosters, meta, m1_model, visc

    @classmethod
    def load(cls, d: Path, m1_model: m1.ThermalModel, visc: m0.ViscosityModel) -> ForecastModel:
        d = Path(d)
        return cls(joblib.load(d / "model.joblib"), json.loads((d / "meta.json").read_text()), m1_model, visc)

    def predict_daily(self, well: dict, steam_t: float, soak_d: float, spm: float, kd: float, cutoff_day: int,
                      cycle_no: int = 1, p_inj: float = 9.0, quality: float = 0.72,
                      scale: float = 1.0, m1_pred: dict | None = None) -> dict[str, Any]:
        """Daily oil (bpd) with P10/P50/P90 for production days a_p..cutoff (actual cycle days)."""
        a_p = 14 + soak_d
        days = np.arange(int(np.ceil(a_p)), int(cutoff_day) + 1, dtype=float)
        if len(days) == 0:
            z = np.zeros(0)
            return {"day": z, "oil": z, "oil_p10": z, "oil_p90": z, "cum_oil": 0.0, "cum_p10": 0.0, "cum_p90": 0.0}
        th = m1_pred or self.m1.predict(steam_t, days, p_inj, quality, soak_d, cycle_no, float(well["steam_eff"]),
                                        quantiles=False)
        X = pd.DataFrame({
            "dprod": days - a_p, "day": days, "steam_t": steam_t, "soak_days": soak_d, "spm": spm, "kd": kd,
            "cycle_no": cycle_no, "pi_factor": well["pi_factor"], "visc_factor": well["visc_factor"],
            "steam_eff": well["steam_eff"], "decline_rate": well["decline_rate"], "m1_T": th["T"],
            "m1_rh": th["rh"], "m1_battery": th["battery"], "inj_pressure_mpa": p_inj, "steam_quality": quality})
        X["prior_oil"] = prior_oil(X["steam_t"], X["dprod"], soak_d, X["steam_eff"], X["pi_factor"])
        X["mu_cp"] = viscosity_for(self.visc, X["m1_T"].to_numpy(), well)
        lr = self.b["mean"].predict(X[FEATS])
        lo = self.b["0.1"].predict(X[FEATS]) - self.meta["cqr"]
        hi = self.b["0.9"].predict(X[FEATS]) + self.meta["cqr"]
        pr = X["prior_oil"].to_numpy() * scale
        oil, p10, p90 = pr * np.exp(lr), pr * np.exp(np.minimum(lo, lr)), pr * np.exp(np.maximum(hi, lr))
        cum = float(np.sum(oil))
        cl, ch = self.meta["cycle_log_q"]
        return {"day": days, "oil": oil, "oil_p10": p10, "oil_p90": p90, "cum_oil": cum,
                "cum_p10": cum * float(np.exp(cl)), "cum_p90": cum * float(np.exp(ch)),
                "model": ID, "version": self.meta["version"], "source": self.meta["source"]}


def well_scale(history: list[tuple[float, float]]) -> float:
    """Per-well Bayesian scaling: shrunken mean log(actual/predicted) of earlier cycles (prior strength 2)."""
    if not history:
        return 1.0
    r = np.log(np.array([max(a, 1.0) / max(p, 1.0) for p, a in history]))
    n = len(r)
    return float(np.exp(n / (n + PRIOR_STRENGTH) * r.mean()))


def train(out_dir: Path, quick: bool = False) -> dict:
    with common.timer() as tm:
        if quick:
            data.ensure_small_data()
        df = features.daily_table(data.cycles(), data.cycle_daily(), data.wells()).reset_index(drop=True)
        n_splits = 2 if quick else 5
        trees = 40 if quick else 250
        folds = features.group_folds(df["well_id"], n_splits)
        visc = m0.ViscosityModel.load(common.model_dir(m0.ID, out_dir)) if (Path(out_dir) / m0.ID / "model.joblib").exists() else None
        if visc is None:
            m0.train(out_dir, quick=True)
            visc = m0.ViscosityModel.load(common.model_dir(m0.ID, out_dir))
        m1_oof = m1.oof_median_predictions(df, folds, 30 if quick else 150)
        X = _feature_frame(df, m1_oof, visc)
        prod = (X["phase"] == "PRODUCTION") & (X["oil_bpd"] > 0.5) & (X["prior_oil"] > 0.1)
        X = X[prod].copy()
        y = np.log(X["oil_bpd"].to_numpy() / X["prior_oil"].to_numpy())
        fo = folds[X.index.to_numpy()]
        oof = {k: np.zeros(len(X)) for k in ("mean", "0.1", "0.9")}
        for k in range(n_splits):
            tr = fo != k
            for kind in oof:
                oof[kind][~tr] = _fit(X[tr], y[tr], kind, trees).predict(X[~tr][FEATS])
        # --- daily CQR
        score = np.maximum(oof["0.1"] - y, y - oof["0.9"])
        cqr = float(np.quantile(score, 0.8))
        # --- cycle level
        X = X.assign(pred=X["prior_oil"] * np.exp(oof["mean"]), lo=X["prior_oil"] * np.exp(np.minimum(oof["0.1"] - cqr, oof["mean"])),
                     hi=X["prior_oil"] * np.exp(np.maximum(oof["0.9"] + cqr, oof["mean"])), fold=fo)
        cyc = X.groupby(["well_id", "cycle_no"]).agg(actual=("oil_bpd", "sum"), pred=("pred", "sum"), lo=("lo", "sum"),
                                                    hi=("hi", "sum"), n=("day", "size"), fold=("fold", "first")).reset_index()
        cm = data.cycles()[["well_id", "cycle_no", "complete"]]
        cyc = cyc.merge(cm, on=["well_id", "cycle_no"])
        cyc = cyc[cyc["complete"] & (cyc["actual"] > 100)].copy()
        cyc["logr"] = np.log(cyc["actual"] / cyc["pred"])
        # arps baseline + per-well scaling (sequential)
        arps_pred, scaled = [], []
        for _, r in cyc.iterrows():
            g = X[(X.well_id == r.well_id)]
            prev = g[g.cycle_no == r.cycle_no - 1]
            cur = g[g.cycle_no == r.cycle_no]
            if len(prev) >= 10:
                arps_pred.append(float(arps_baseline(prev["dprod"].to_numpy(), prev["oil_bpd"].to_numpy(),
                                                     cur["dprod"].to_numpy()).sum()))
            else:
                arps_pred.append(np.nan)
            hist = cyc[(cyc.well_id == r.well_id) & (cyc.cycle_no < r.cycle_no)]
            scaled.append(r["pred"] * well_scale(list(zip(hist["pred"], hist["actual"], strict=True))))
        cyc["arps"], cyc["scaled"] = arps_pred, scaled
        mape = lambda a, p: float(np.mean(np.abs(p - a) / a) * 100)  # noqa: E731
        has = cyc["arps"].notna()
        met: dict = {"cycle_mape_ml_pct": mape(cyc["actual"], cyc["pred"]),
               "cycle_mape_ml_with_well_scaling_pct": mape(cyc["actual"], cyc["scaled"]),
               "cycle_mape_arps_pct": mape(cyc.loc[has, "actual"], cyc.loc[has, "arps"]),
               "cycle_mape_ml_same_subset_pct": mape(cyc.loc[has, "actual"], cyc.loc[has, "pred"]),
               "daily_mape_ml_pct": float(np.mean(np.abs(X["pred"] - X["oil_bpd"]) / X["oil_bpd"]) * 100),
               "n_cycles": int(len(cyc)), "n_cycles_with_prev": int(has.sum()),
               "daily_cover80": float(np.mean((X["oil_bpd"] >= X["lo"]) & (X["oil_bpd"] <= X["hi"])))}
        # split-conformal coverage on held-out wells, repeated random splits
        wl = cyc["well_id"].unique()
        rg = np.random.default_rng(0)
        cov: list[float] = []
        for _ in range(200):
            p = rg.permutation(wl)
            cal, tst = set(p[: len(p) // 2]), set(p[len(p) // 2:])
            lc = cyc[cyc.well_id.isin(cal)]["logr"].to_numpy()
            lt = cyc[cyc.well_id.isin(tst)]["logr"].to_numpy()
            if len(lc) < 5 or len(lt) < 3:
                continue
            ql, qh = np.quantile(lc, [0.1, 0.9])
            cov.append(np.mean((lt >= ql) & (lt <= qh)))
        met["cycle_cover80_mean"] = float(np.mean(cov)) if cov else None
        met["cycle_cover80_std"] = float(np.std(cov)) if cov else None
        ql, qh = (float(v) for v in np.quantile(cyc["logr"], [0.1, 0.9]))
        boosters = {kind: _fit(X, y, kind, trees) for kind in oof}
        meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "features": FEATS,
                "trained_at": common.now_iso(), "cqr": cqr, "cycle_log_q": [ql, qh], "n_rows": len(X),
                "data_hash": common.data_hash([X[FEATS]])}
    d = common.model_dir(ID, out_dir)
    joblib.dump(boosters, d / "model.joblib", compress=3)
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "cycle_cum_oil_mape_pct", "value": met["cycle_mape_ml_pct"], "target": 10.0,
                                     "baseline_name": "arps_prev_cycle", "baseline": met["cycle_mape_arps_pct"],
                                     "direction": "lower"},
          "secondary": {"name": "cycle_cover80", "value": met["cycle_cover80_mean"], "target_range": [0.78, 0.82]},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"],
          "data_hash": meta["data_hash"], "quick": quick, "cv": f"{n_splits}-fold grouped by well",
          "notes": ["baseline is evaluated on the cycles with a previous cycle; the like-for-like ML number is cycle_mape_ml_same_subset_pct"]}
    card = f"""# M2 cycle production forecaster
Daily oil = physics prior (twin Boberg-Lantz rate x PI) x exp(LightGBM residual); P10/P90 from CQR (daily) and split-conformal
(cycle cum oil). **Source: physics_synthetic** (S2). S2 cycles carry a 6 % lognormal cycle-to-cycle noise that no model can
predict, so about 5 % MAPE is the floor on this data.
- {ev["cv"]}; M1 inputs out-of-fold. Metrics: {json.dumps(met)}
- Baseline: Arps hyperbolic on the previous cycle (blind to steam/soak/pump changes). Targets: cycle cum-oil MAPE <= 10 %, 80 % interval coverage 0.78-0.82.
- Per-well Bayesian scaling (prior strength 2) is applied at inference via ``scale=well_scale(history)``.
- Limits: trained on the 60-well roster; production-days only; requires M0 and M1 artifacts at inference.
"""
    return common.write_eval(d, ID, ev, card)
