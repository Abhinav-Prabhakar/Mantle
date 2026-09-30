"""M4 failure & unseat risk: gradient-boosted Cox survival (scikit-survival) + per-rod Miner's-rule localisation.

Unit of analysis = one production period of a cycle (time = days since production start; event = first rod part /
first pump unseat, else censored at the last observed day). Covariates come from S2 daily rows (twin-derived Goodman,
float margin, fillage -> impacts and impact velocity, viscosity -> uplift) plus well properties and time since the
last workover. Baseline: Weibull on run time only. Per-rod: modified-Goodman profile -> Miner damage (mantle_physics.hazard).
Optional LLM text features (L3/L4/L5 TF-IDF -> SVD) are appended when ``data/llm/L[345]*.jsonl`` exist.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sksurv.metrics import brier_score, concordance_index_censored
from sksurv.util import Surv

from mantle_physics import WellSim
from mantle_physics.constants import S_M
from mantle_physics.hazard import (
    N_RODS,
    ROD_LENGTH_M,
    pump_uplift_kn,
    rod_damage_rate,
    rod_failure_probability,
)

from .. import common, data, features
from .. import fasttwin as ft

ID = "M4"
COV = ["goodman_mean", "goodman_max", "gr_eff", "float_frac", "impacts_day", "impact_vel", "mu_mean", "uplift_mean", "uplift_max",
       "spm", "kd", "corrosion", "stress_factor", "cycle_no", "steam_t", "days_since_workover", "cum_kstrokes", "prior_unseat_rate", "prior_rod_rate",
       "hold_down_kn", "uplift_ratio_mean", "uplift_ratio_max"]
# Covariates an operating change (spm / kd) moves. Everything else is well or history (corrosion, rod stress factor, hold-down,
# cycle number, run-time since workover, cumulated strokes, event history) and must be identical in a "with Mantle" evaluation.
OPERATING_COV = ("goodman_mean", "goodman_max", "gr_eff", "float_frac", "impacts_day", "impact_vel", "uplift_mean", "uplift_max",
                 "uplift_ratio_mean", "uplift_ratio_max", "spm", "kd")
RANGE_COV = ("goodman_mean", "goodman_max", "gr_eff", "float_frac", "impacts_day", "impact_vel", "mu_mean", "uplift_mean",
             "uplift_max", "uplift_ratio_mean", "uplift_ratio_max", "spm", "kd", "steam_t")
HORIZON = 30.0


# ---------------------------------------------------------------- covariates


def cycle_covariates(daily: pd.DataFrame, cyc: pd.DataFrame, wells: pd.DataFrame, workovers: pd.DataFrame) -> pd.DataFrame:
    p = daily[daily["phase"] == "PRODUCTION"].merge(cyc[["well_id", "cycle_no", "spm", "kd", "steam_t", "start_date", "soak_days"]],
                                                    on=["well_id", "cycle_no"])
    fill = p["fillage"].to_numpy()
    p["pound"] = np.clip((0.85 - fill) / 0.35, 0, 1)
    p["impacts"] = p["spm"] * 1440 * p["pound"]
    p["ivel"] = (0.15 + (1 - fill) * 1.3) * p["spm"] / 5.4
    p["ffrac"] = np.clip((0.15 - p["float_margin"]) / 0.3, 0, 1)
    p["uplift"] = pump_uplift_kn(p["viscosity_cp"].to_numpy(), np.pi * S_M * p["spm"].to_numpy() / 60, fill)
    g = p.groupby(["well_id", "cycle_no"])
    out = g.agg(goodman_mean=("goodman", "mean"), goodman_max=("goodman", "max"), float_frac=("ffrac", "mean"),
                impacts_day=("impacts", "mean"), impact_vel=("ivel", "mean"), mu_mean=("viscosity_cp", "mean"),
                uplift_mean=("uplift", "mean"), uplift_max=("uplift", "max"), spm=("spm", "first"), kd=("kd", "first"), steam_t=("steam_t", "first"),
                start_date=("start_date", "first"), soak_days=("soak_days", "first"), n_prod=("day", "size")).reset_index()
    w = wells.set_index("well_id")
    out["corrosion"] = out["well_id"].map(w["corrosion_index"])
    out["stress_factor"] = out["well_id"].map(w["rod_stress_factor"])
    out["gr_eff"] = out["goodman_mean"] * out["stress_factor"]
    out["hold_down_kn"] = out["well_id"].map(w["hold_down_kn"])
    out["uplift_ratio_mean"] = out["uplift_mean"] / out["hold_down_kn"]
    out["uplift_ratio_max"] = out["uplift_max"] / out["hold_down_kn"]
    # days since the last workover of any kind before this cycle's production start (else since 1 year before start)
    wo = workovers.groupby("well_id")["date"].apply(lambda s: sorted(pd.to_datetime(s)))
    dsw, cum = [], []
    for r in out.itertuples():
        t0 = pd.Timestamp(r.start_date) + pd.Timedelta(days=14 + float(r.soak_days))
        prev = [d for d in wo.get(r.well_id, []) if d < t0]
        last = prev[-1] if prev else t0 - pd.Timedelta(days=365)
        days = float((t0 - last).days)
        dsw.append(days)
        cum.append(days * r.spm * 1440 / 1000)
    out["days_since_workover"], out["cum_kstrokes"] = dsw, cum
    return out


def event_table(cov: pd.DataFrame, cycles: pd.DataFrame, fails: pd.DataFrame, unseats: pd.DataFrame) -> pd.DataFrame:
    """One row per production period with time-to-first rod part / unseat (days since production start)."""
    key = cycles.set_index(["well_id", "cycle_no"])[["start_date", "soak_days"]]

    def a_p(w, n):
        return 14.0 + float(key.loc[(w, n), "soak_days"]) if (w, n) in key.index else np.nan

    rod = fails[fails["kind"] == "rod_part"].dropna(subset=["cycle_no"]).copy()
    rod["t"] = [(pd.Timestamp(r.date) - pd.Timestamp(key.loc[(r.well_id, int(r.cycle_no)), "start_date"])).days - a_p(r.well_id, int(r.cycle_no))
                if (r.well_id, int(r.cycle_no)) in key.index else np.nan for r in rod.itertuples()]
    un = unseats.dropna(subset=["cycle_no"]).copy()
    un["t"] = [r.cycle_day - a_p(r.well_id, int(r.cycle_no)) for r in un.itertuples()]
    rod["cycle_no"], un["cycle_no"] = rod["cycle_no"].astype(int), un["cycle_no"].astype(int)
    c = cov.set_index(["well_id", "cycle_no"])
    c["t_rod"] = rod.groupby(["well_id", "cycle_no"])["t"].min().reindex(c.index)
    c["t_unseat"] = un.groupby(["well_id", "cycle_no"])["t"].min().reindex(c.index)
    c["T"] = c["n_prod"].astype(float)
    c = c.reset_index().sort_values(["well_id", "cycle_no"])
    # well history (frailty proxy): shrunken event rates per 100 production days over EARLIER cycles of the same well
    n_un = un.groupby(["well_id", "cycle_no"]).size()
    n_rod = rod.groupby(["well_id", "cycle_no"]).size()
    c["_nu"] = [float(n_un.get((w, n), 0)) for w, n in zip(c["well_id"], c["cycle_no"], strict=True)]
    c["_nr"] = [float(n_rod.get((w, n), 0)) for w, n in zip(c["well_id"], c["cycle_no"], strict=True)]
    g = c.groupby("well_id")
    days_prev = g["T"].cumsum() - c["T"]
    c["prior_unseat_rate"] = (g["_nu"].cumsum() - c["_nu"] + 0.3) / (days_prev + 100) * 100
    c["prior_rod_rate"] = (g["_nr"].cumsum() - c["_nr"] + 0.3) / (days_prev + 100) * 100
    return c.drop(columns=["_nu", "_nr"]).reset_index(drop=True)


def survival_xy(ev: pd.DataFrame, kind: str) -> np.ndarray:
    t = ev[f"t_{kind}"].to_numpy(dtype=float)
    T = ev["T"].to_numpy(dtype=float)
    event = np.isfinite(t) & (t <= T)
    time = np.where(event, np.maximum(t, 0.5), np.maximum(T, 0.5))
    return Surv.from_arrays(event, time)


# ---------------------------------------------------------------- baseline: Weibull on run time only


def weibull_fit(y) -> tuple[float, float]:
    ev, t = y["event"], y["time"]

    def nll(p):
        k, lam = np.exp(p)
        z = (t / lam) ** k
        return -(np.sum(ev * (np.log(k) - np.log(lam) + (k - 1) * np.log(t / lam))) - np.sum(z))

    r = minimize(nll, [0.0, np.log(max(np.median(t), 1.0) * 2)], method="Nelder-Mead")
    k, lam = np.exp(r.x)
    return float(k), float(lam)


def weibull_surv(k: float, lam: float, t) -> np.ndarray:
    return np.exp(-((np.asarray(t, dtype=float) / lam) ** k))


# ---------------------------------------------------------------- per-rod fatigue


def rod_goodman_profile(peak: float, stress_factor: float, spm: float, kd: float, steam: float, day: float) -> np.ndarray:
    prof = WellSim(spm=spm, cycle_day=min(max(day, 19), 120), kd=kd, steam=steam).profile()
    depth, stress = np.array(prof.depth), np.array(prof.rod_stress)
    z = (np.arange(N_RODS) + 0.5) * ROD_LENGTH_M
    s = np.interp(z, depth, stress)
    top = max(float(stress[depth < 1068].max()), 1e-9)
    return stress_factor * peak * np.clip(s / top, 0, 1)


def rod_fatigue(cov: dict, day_in_prod: float, *, steam: float | None = None, day_twin: float = 60.0) -> dict:
    """Per-rod Miner damage so far in this production period, damage rate and 30-day failure probability."""
    gr = rod_goodman_profile(cov["goodman_mean"], cov["stress_factor"], cov["spm"], cov["kd"], steam or cov["steam_t"], day_twin)
    rate = rod_damage_rate(gr, cov["spm"] * 1440, cov["float_frac"], cov["impacts_day"], cov["impact_vel"], cov["corrosion"])
    dmg = rate * max(day_in_prod, 0.0)
    p30 = rod_failure_probability(dmg, rate, HORIZON)
    return {"goodman": gr, "damage_rate": rate, "damage": dmg, "p30": p30}


def top_rods(fat: dict, k: int = 5) -> list[dict]:
    share = fat["damage_rate"] ** 8
    share = share / max(share.sum(), 1e-30)
    order = np.argsort(-fat["p30"] - 1e-9 * share)[:k]
    return [{"rod": int(i), "depth_m": float((i + 0.5) * ROD_LENGTH_M), "p30": float(fat["p30"][i]), "share": float(share[i]),
             "damage": float(fat["damage"][i]), "goodman": float(fat["goodman"][i])} for i in order]


# ---------------------------------------------------------------- model


def _surv_at(model: GradientBoostingSurvivalAnalysis, X: pd.DataFrame, times) -> np.ndarray:
    S = model.predict_survival_function(X, return_array=True)
    ut = np.asarray(model.unique_times_)
    times = np.atleast_1d(times)
    idx = np.searchsorted(ut, times, side="right") - 1
    out = np.where(idx[None, :] >= 0, S[:, np.clip(idx, 0, None)], 1.0)
    return out


def cov_from_settings(well: dict, steam: float, spm: float, kd: float, cycle_no: int = 1, days_since_workover: float = 90.0,
                      soak: float = 4.0, history_spm: float | None = None, history: dict | None = None) -> dict:
    """Cycle-average covariates for a planned/what-if operating point (uses the vectorised twin).

    Only the operating covariates (``OPERATING_COV``) depend on ``spm``/``kd``. ``history_spm`` is the pump speed the well has
    actually run since its last workover: the cumulated strokes are history and do not change with a what-if speed.
    ``history`` overrides the well-history covariates (e.g. ``prior_unseat_rate`` / ``prior_rod_rate`` from the well's records)."""
    r = ft.cycle_days(steam, spm, kd, steam_eff=float(well.get("steam_eff", 1.0)), k_oil=float(well.get("pi_factor", 1.0)))
    sl = slice(18, 111)
    fill = r["fill"][sl]
    pound = np.clip((0.85 - fill) / 0.35, 0, 1)
    mu = r["mu"][sl] * float(well.get("visc_factor", 1.0))
    gm = float(r["goodman"][sl].mean())
    up = pump_uplift_kn(mu, np.pi * S_M * spm / 60, fill)
    hd = float(well.get("hold_down_kn", 26.0))
    cov = {"goodman_mean": gm, "goodman_max": float(r["goodman"][sl].max()), "gr_eff": gm * float(well["rod_stress_factor"]),
           "float_frac": float(np.clip((0.15 - r["margin"][sl]) / 0.3, 0, 1).mean()),
           "impacts_day": float((spm * 1440 * pound).mean()), "impact_vel": float(((0.15 + (1 - fill) * 1.3) * spm / 5.4).mean()),
           "mu_mean": float(mu.mean()), "uplift_mean": float(up.mean()), "uplift_max": float(up.max()),
           "spm": spm, "kd": kd, "corrosion": float(well["corrosion_index"]), "stress_factor": float(well["rod_stress_factor"]),
           "cycle_no": cycle_no, "steam_t": steam, "days_since_workover": days_since_workover,
           "cum_kstrokes": days_since_workover * (spm if history_spm is None else history_spm) * 1440 / 1000,
           "hold_down_kn": hd, "uplift_ratio_mean": float(up.mean()) / hd, "uplift_ratio_max": float(up.max()) / hd}
    cov.update(history or {})
    return cov


class RiskModel:
    """Cox models for first rod part / first unseat. ``rod_ens`` / ``unseat_ens`` are the cross-validation fold models
    (each fitted on ~80 % of the wells): their spread is the model uncertainty reported with every MTBF."""

    def __init__(self, rod, unseat, meta: dict, rod_ens=None, unseat_ens=None):
        self.rod, self.unseat, self.meta = rod, unseat, meta
        self.rod_ens, self.unseat_ens = list(rod_ens or []), list(unseat_ens or [])

    @classmethod
    def load(cls, d: Path) -> RiskModel:
        d = Path(d)
        z = joblib.load(d / "model.joblib")
        return cls(z["rod"], z["unseat"], json.loads((d / "meta.json").read_text()), z.get("rod_ens"), z.get("unseat_ens"))

    def clip(self, cov: dict) -> tuple[dict, list[str]]:
        """Clamp covariates to the training distribution (1st-99th percentile): a tree ensemble is flat outside it, so an
        out-of-range what-if would otherwise read as a spurious step. Returns the clipped covariates and the names clipped."""
        out, hit = dict(cov), []
        for k, (lo, hi) in self.meta.get("ranges", {}).items():
            if k in out and np.isfinite(out[k]) and not lo <= out[k] <= hi:
                out[k] = float(np.clip(out[k], lo, hi))
                hit.append(k)
        return out, hit

    def _x(self, cov: dict) -> pd.DataFrame:
        row = {k: float(cov.get(k, self.meta["defaults"].get(k, 0.0))) for k in self.meta["features"]}
        return pd.DataFrame([row])[self.meta["features"]]

    @staticmethod
    def _risk_hazard(m, X: pd.DataFrame, t0: float) -> tuple[float, float]:
        """(P(event in the next 30 d | survived to t0), mean hazard per day over those 30 d). The hazard is the 30-day cumulative
        hazard / 30: a 1-day difference of the Cox step function is 0 almost everywhere."""
        s = _surv_at(m, X, np.array([t0, t0 + HORIZON]))[0]
        r = float(np.clip(1 - s[1] / max(s[0], 1e-9), 0, 1))
        return r, float(-np.log(max(1 - r, 1e-9)) / HORIZON)

    def assess(self, cov: dict, day_in_prod: float, *, steam: float | None = None, day_twin: float = 60.0) -> dict:
        """30-day rod-part / unseat risk (conditional on surviving to ``day_in_prod``), hazard, MTBF (+ P10-P90 over the fold
        ensemble), per-rod localisation. Covariates outside the training range are clipped (``extrapolated`` names them)."""
        raw = cov
        cov, hit = self.clip(cov)
        X = self._x(cov)
        t0 = max(float(day_in_prod), 0.5)
        out: dict[str, Any] = {}
        haz = 0.0
        for name, m in (("rod", self.rod), ("unseat", self.unseat)):
            risk, h = self._risk_hazard(m, X, t0)
            out[f"risk_30d_{name}"], out[f"hazard_per_day_{name}"] = risk, h
            haz += h
        out["risk_30d"] = 1 - (1 - out["risk_30d_rod"]) * (1 - out["risk_30d_unseat"])
        out["hazard_per_day"] = haz
        out["mtbf_days"] = _mtbf(haz)
        ens = self.member_hazards(X, t0)
        if len(ens):
            m_ = np.array([_mtbf(h) for h in ens])
            out["mtbf_p10"], out["mtbf_p90"] = float(np.percentile(m_, 10)), float(np.percentile(m_, 90))
        out["extrapolated"] = hit
        fat = rod_fatigue(raw, day_in_prod, steam=steam, day_twin=day_twin)
        out["rods_damage"] = fat["damage"]
        out["top_rods"] = top_rods(fat)
        out.update({"model": ID, "version": self.meta["version"], "source": self.meta["source"]})
        return out

    def member_hazards(self, X: pd.DataFrame, t0: float) -> np.ndarray:
        """Combined (rod + unseat) daily hazard of every fold-model pair."""
        n = min(len(self.rod_ens), len(self.unseat_ens))
        return np.array([self._risk_hazard(self.rod_ens[i], X, t0)[1] + self._risk_hazard(self.unseat_ens[i], X, t0)[1]
                         for i in range(n)])

    def compare(self, cov_now: dict, cov_new: dict, day_in_prod: float, *, steam: float | None = None,
                day_twin: float = 60.0) -> dict:
        """MTBF now vs under ``cov_new`` (same well and history, only the operating covariates differ), with the ratio's P10-P90
        across the fold ensemble (each member compared with itself, so shared model error cancels)."""
        a = self.assess(cov_now, day_in_prod, steam=steam, day_twin=day_twin)
        b = self.assess(cov_new, day_in_prod, steam=steam, day_twin=day_twin)
        t0 = max(float(day_in_prod), 0.5)
        ha = self.member_hazards(self._x(self.clip(cov_now)[0]), t0)
        hb = self.member_hazards(self._x(self.clip(cov_new)[0]), t0)
        ratios = np.array([_mtbf(y) / _mtbf(x) for x, y in zip(ha, hb, strict=True)]) if len(ha) else np.array([])
        ratio = b["mtbf_days"] / a["mtbf_days"]
        return {"now": a, "new": b, "mtbf_ratio": float(ratio),
                "mtbf_ratio_p10": float(np.percentile(ratios, 10)) if len(ratios) else None,
                "mtbf_ratio_p90": float(np.percentile(ratios, 90)) if len(ratios) else None,
                "extrapolated": sorted(set(a["extrapolated"]) | set(b["extrapolated"]))}


MTBF_CAP_DAYS = 5000.0


def _mtbf(hazard_per_day: float) -> float:
    return float(min(1.0 / max(hazard_per_day, 1e-6), MTBF_CAP_DAYS))


def _fit(X: pd.DataFrame, y, quick: bool) -> GradientBoostingSurvivalAnalysis:
    m = GradientBoostingSurvivalAnalysis(n_estimators=40 if quick else 120, max_depth=2, learning_rate=0.08, subsample=0.8,
                                         min_samples_leaf=8, random_state=0)
    return m.fit(X, y)


def build_events(quick: bool) -> pd.DataFrame:
    if quick:
        data.ensure_small_data()
    cyc, daily, wells = data.cycles(), data.cycle_daily(), data.wells()
    cov = cycle_covariates(daily, cyc, wells, data.workovers())
    ev = event_table(cov, cyc, data.failures(), data.unseats())
    txt = features.llm_text_features(list(wells["well_id"]))
    if txt is not None:
        ev = ev.merge(txt, on="well_id", how="left").fillna(0.0)
    return ev


def train(out_dir: Path, quick: bool = False) -> dict:
    with common.timer() as tm:
        ev = build_events(quick)
        feats = COV + [c for c in ev.columns if c.startswith("txt")]
        folds = features.group_folds(ev["well_id"], 3 if quick else 5)
        met: dict = {"n_cycles": int(len(ev))}
        res: dict[str, dict] = {}
        models: dict = {}
        for kind in ("rod", "unseat"):
            models[f"{kind}_ens"] = []
            y = survival_xy(ev, kind)
            X = ev[feats]
            met[f"n_events_{kind}"] = int(y["event"].sum())
            risk = np.zeros(len(ev))
            s30_ml, s30_wb, tt = np.full(len(ev), np.nan), np.full(len(ev), np.nan), 30.0
            for k in np.unique(folds):
                tr, te = folds != k, folds == k
                if y["event"][tr].sum() < 3:
                    continue
                m = _fit(X[tr], y[tr], quick)
                models[f"{kind}_ens"].append(m)
                risk[te] = m.predict(X[te])
                s30_ml[te] = _surv_at(m, X[te], np.array([tt]))[:, 0]
                kk, lam = weibull_fit(y[tr])
                s30_wb[te] = weibull_surv(kk, lam, tt)
            ok = ~np.isnan(s30_ml)
            if ok.sum() < 5 or y["event"][ok].sum() < 2:       # degenerate quick-mode data
                res[kind] = {"c_index_ml": float("nan"), "c_index_age_baseline": float("nan")}
                models[kind] = _fit(X, y, quick)
                continue
            c_ml = concordance_index_censored(y["event"][ok], y["time"][ok], risk[ok])[0]
            c_age = concordance_index_censored(y["event"][ok], y["time"][ok], ev["days_since_workover"].to_numpy()[ok])[0]
            bs: dict = {}
            try:
                # IPCW Brier at 30 d needs follow-up beyond 30 d in the test data; use pooled OOF predictions
                yy = y[ok]
                tmax = float(yy["time"].max())
                t_eval = min(tt, 0.95 * tmax)
                b_ml = brier_score(yy, yy, s30_ml[ok], t_eval)[1][0]
                b_wb = brier_score(yy, yy, s30_wb[ok], t_eval)[1][0]
                bs = {"brier_30d_ml": float(b_ml), "brier_30d_weibull": float(b_wb), "brier_improvement": float(1 - b_ml / b_wb)}
            except Exception as e:  # pragma: no cover - degenerate quick data
                bs = {"brier_error": str(e)[:80]}
            res[kind] = {"c_index_ml": float(c_ml), "c_index_age_baseline": float(c_age), **bs}
            models[kind] = _fit(X, y, quick)
        met.update({f"{k}_{m}": v for k, d in res.items() for m, v in d.items()})
        # localisation: top-3 hit rate of the physics ranking on S5 rod failures (same physics generated them)
        met["rod_top3_hit"], met["rod_top3_random"] = _localisation(ev, quick)
    d = common.model_dir(ID, out_dir)
    joblib.dump(models, d / "model.joblib", compress=3)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "features": feats,
            "trained_at": common.now_iso(), "n_cycles": int(len(ev)), "data_hash": common.data_hash([ev[COV]]),
            "defaults": {c: float(ev[c].mean()) for c in feats},
            "ranges": {c: [float(ev[c].quantile(0.005)), float(ev[c].quantile(0.995))] for c in RANGE_COV},
            "text_features": any(c.startswith("txt") for c in feats)}
    (d / "meta.json").write_text(json.dumps(meta))
    r = res["rod"]
    evd = {"metrics": met, "primary": {"name": "c_index_rod", "value": r["c_index_ml"], "target": 0.75,
                                      "baseline_name": "weibull_age", "baseline": r["c_index_age_baseline"], "direction": "higher",
                                      "secondary": {"name": "brier_improvement_30d", "value": r.get("brier_improvement"),
                                                    "target": 0.20}},
           "notes": [f"Unseat model: C-index {res['unseat']['c_index_ml']:.2f} (target 0.75) and Brier(30 d) improvement "
                     f"{res['unseat'].get('brier_improvement', float('nan')):.2f}: MISSED. Unseats are rare after the S5 recalibration (~0.8 per well-year), "
                     "and only the first unseat per production period is modelled."],
           "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"],
           "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# M4 failure & unseat risk
Gradient-boosted Cox survival models (scikit-survival) for first rod part and first pump unseat per production period, plus Miner's-rule per-rod localisation.
**Source: physics_synthetic** (S2 covariates, S5 event histories generated from the same hazard physics; {len(ev)} production periods). Because S5 is
simulated from the physics hazard, high C-index shows the model recovers that hazard, not real failure behaviour. Text features from LLM records: {"used" if meta["text_features"] else "not used (no data/llm L3/L4/L5 files)"}.
- Covariates: {", ".join(COV)}. 5-fold CV grouped by well. Metrics: {json.dumps(met)}
- Baseline: Weibull on run time only (Brier at 30 d) and days-since-workover as the age-only risk score (C-index; a marginal Weibull has C=0.5).
- Per-rod: Goodman-by-depth profile x stress factor -> Miner damage rate; top rods = highest 30-day failure probability. Top-3 hit rate on S5 failures is reported but is partly circular (same physics).
- Unseat model MISSES its targets (rare events, first per production period only); see eval.json notes.
- MTBF = 1 / (rod + unseat hazard), each hazard the 30-day cumulative hazard / 30 (a 1-day difference of the Cox step function is ~0). Covariates are clipped to the 0.5-99.5 % training range (`meta.ranges`, reported as `extrapolated`). The uncertainty is the spread of the cross-validation fold models (P10-P90). A "with Mantle" MTBF (`compare`) changes only the operating covariates (goodman, float, impacts, uplift, spm, kd); well and history covariates (corrosion, hold-down, age, strokes so far, event record) are identical.
- Limits: cycle-average covariates; first event per period only; exponential MTBF approximation; S3 telemetry not used (only 20 wells).
"""
    return common.write_eval(d, ID, evd, card)


def _localisation(ev: pd.DataFrame, quick: bool) -> tuple[float | None, float]:
    fails = data.failures()
    fails = fails[fails["kind"] == "rod_part"].dropna(subset=["rod_index", "cycle_no"])
    cov = ev.set_index(["well_id", "cycle_no"])
    wells = data.wells().set_index("well_id")
    rows = fails.sample(min(len(fails), 40 if quick else 250), random_state=0) if len(fails) else fails
    hit, n = 0, 0
    for r in rows.itertuples():
        key = (r.well_id, r.cycle_no)
        if key not in cov.index:
            continue
        c = cov.loc[key]
        d = c.to_dict()
        d["stress_factor"] = float(wells.loc[r.well_id, "rod_stress_factor"])
        fat = rod_fatigue(d, 50.0, day_twin=float(c["n_prod"]) / 2 + 18)
        top = [t["rod"] for t in top_rods(fat, 3)]
        hit += int(int(r.rod_index) in top)
        n += 1
    return (hit / n if n else None), 3 / N_RODS

