"""O1 SRP controller: constrained optimisation of (spm, kd) on the physics twin (+M5 impact law, physics risk cost).

maximise   oil value - energy cost - risk cost        (INR/day at the current cycle day)
subject to float margin >= 0.15, fillage >= 0.8, Goodman <= 0.9, torque <= 1.0
Method: vectorised grid over spm x kd as warm start, then SciPy SLSQP refinement; the tabulated twin core
(``fasttwin``) makes one call ~ms. Baseline: today's fixed SPM. Output shape = twin ``recommendation`` + hz + impacts delta.
Risk cost: Miner's-rule rod-part hazard (140 rods) and pump-unseat hazard from ``mantle_physics.hazard`` (the same
laws that generated S5 and that M4 is trained on) times S5-like job costs; M4 (survival) reports the resulting 30-day
risk of the chosen setting when a risk model is supplied.
"""

from __future__ import annotations

import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from mantle_physics.constants import CYCLE_DAYS, MARGIN_REQ, PRICE, S_M, SOAK_END
from mantle_physics.hazard import WEIBULL_K, pump_unseat_hazard, pump_uplift_kn, rod_damage_rate

from .. import common
from .. import fasttwin as ft
from . import m5_stroke

ID = "O1"
KD_LO, KD_HI = 0.40, 0.70
SPM_LO, SPM_HI = 0.8, 9.0
SPM_GRID = np.round(np.arange(SPM_LO, SPM_HI + 1e-6, 0.2), 2)
KD_GRID = np.round(np.arange(0.40, 0.7001, 0.02), 3)
C_ROD, C_UNSEAT = 4.5e5, 2.0e5           # INR per job (S5 average rig + material cost)
LIMITS = {"margin": MARGIN_REQ, "fill": 0.8, "goodman": 0.9, "torque": 1.0}
DEFAULT_WELL = {"steam_eff": 1.0, "pi_factor": 1.0, "visc_factor": 1.0, "rod_stress_factor": 1.2, "corrosion_index": 0.35,
                "hold_down_kn": 26.0}


@lru_cache(maxsize=1)
def rod_shape() -> np.ndarray:
    from .m4_risk import rod_goodman_profile

    return rod_goodman_profile(1.0, 1.0, 5.4, 0.5, 800.0, 60.0)


def base_state(steam: float, day: float, well: dict) -> dict[str, float]:
    b = ft.base_at(ft.eff_steam(steam, float(well["steam_eff"])))
    d = float(np.clip(day, 0, CYCLE_DAYS))
    i0 = min(int(d), CYCLE_DAYS - 1)
    f = d - i0
    return {n: float(ft.base_field(b, n)[i0] * (1 - f) + ft.base_field(b, n)[i0 + 1] * f) for n in ("qIn", "wc", "c", "c500", "c800", "muPump")}


def evaluate(bs: dict[str, float], well: dict, spm, kd, t_prod: float, price_oil: float = PRICE["oil"],
             kwh_price: float = PRICE["kwh"]) -> dict[str, np.ndarray]:
    """Vectorised state for arrays ``spm``/``kd`` (broadcast): twin core + impacts + risk cost + objective (INR/day)."""
    k_oil = float(well["pi_factor"])
    r = ft.core(bs["qIn"] * k_oil, bs["wc"], bs["c"], bs["c500"], bs["c800"], spm, kd)   # PI scales the inflow itself
    fill = r["fill"]
    imp = m5_stroke.impacts_per_day(spm, fill)
    ivel = m5_stroke.impact_velocity(spm, fill)
    # rod hazard: sum_i k * rate_i^k * t^(k-1)  (damage grows linearly with rate)
    gr = rod_shape() * r["goodman"][..., None] * float(well["rod_stress_factor"])
    sp = np.asarray(spm, dtype=float)[..., None]
    rate = rod_damage_rate(gr, sp * 1440, 0.0, np.asarray(imp)[..., None], np.asarray(ivel)[..., None], float(well["corrosion_index"]))
    rod_h = np.sum(WEIBULL_K * np.maximum(rate * max(t_prod, 5.0), 1e-12) ** (WEIBULL_K - 1) * rate, axis=-1)
    mu = bs["muPump"] * float(well["visc_factor"])
    uplift = pump_uplift_kn(mu, np.pi * S_M * np.asarray(spm) / 60, fill, ivel)
    un_h = pump_unseat_hazard(uplift, float(well["hold_down_kn"]))
    oil = r["oil"]
    rod_h, un_h = np.minimum(rod_h, 1.0), np.minimum(un_h, 1.0)      # per-day probabilities
    risk_cost = rod_h * (C_ROD + 2 * 24 * oil * price_oil / 24) + un_h * (C_UNSEAT + oil * price_oil)
    value = oil * price_oil - r["kw"] * 24 * kwh_price
    return {**r, "impacts": imp, "impact_vel": ivel, "rod_hazard": rod_h, "unseat_hazard": un_h, "risk_cost": risk_cost,
            "value": value, "objective": value - risk_cost}


def _feasible(e: dict) -> np.ndarray:
    return ((e["margin_raw"] >= LIMITS["margin"]) & (e["fill"] >= LIMITS["fill"]) & (e["goodman"] <= LIMITS["goodman"])
            & (e["torque"] <= LIMITS["torque"]))


def _violation(e: dict) -> np.ndarray:
    return (np.maximum(0, LIMITS["margin"] - e["margin_raw"]) + np.maximum(0, LIMITS["fill"] - e["fill"])
            + np.maximum(0, e["goodman"] - LIMITS["goodman"]) + np.maximum(0, e["torque"] - LIMITS["torque"]))


def optimise_point(bs: dict[str, float], well: dict, t_prod: float, price_oil: float = PRICE["oil"], refine: bool = True
                   ) -> dict[str, Any]:
    S, K = np.meshgrid(SPM_GRID, KD_GRID, indexing="ij")
    e = evaluate(bs, well, S, K, t_prod, price_oil)
    feas = _feasible(e)
    if feas.any():
        obj = np.where(feas, e["objective"], -np.inf)
        j = np.unravel_index(int(np.argmax(obj)), obj.shape)
        ok = True
    else:
        j = np.unravel_index(int(np.argmax(e["objective"] - 3e5 * _violation(e))), S.shape)   # soft-penalised best
        ok = False
    x0 = np.array([S[j], K[j]])
    best_x, best_e = x0, {k: float(np.asarray(v)[j]) for k, v in e.items() if np.ndim(v) == 2}
    if refine and ok:
        cache: dict[tuple, dict] = {}

        def ev(x):
            key = (round(float(x[0]), 9), round(float(x[1]), 9))
            if key not in cache:
                cache[key] = {k: float(np.asarray(v)) for k, v in evaluate(bs, well, np.array(x[0]), np.array(x[1]), t_prod, price_oil).items()
                              if np.ndim(v) == 0 or np.size(v) == 1}
            return cache[key]

        cons = [{"type": "ineq", "fun": lambda x: ev(x)["margin_raw"] - LIMITS["margin"]},
                {"type": "ineq", "fun": lambda x: ev(x)["fill"] - LIMITS["fill"]},
                {"type": "ineq", "fun": lambda x: LIMITS["goodman"] - ev(x)["goodman"]},
                {"type": "ineq", "fun": lambda x: LIMITS["torque"] - ev(x)["torque"]}]
        try:
            res = minimize(lambda x: -ev(x)["objective"] / 1000.0, x0, method="SLSQP", constraints=cons,
                           bounds=[(SPM_LO, SPM_HI), (KD_LO, KD_HI)], options={"maxiter": 30, "ftol": 1e-7})
            x = np.array([float(np.clip(res.x[0], SPM_LO, SPM_HI)), float(np.clip(res.x[1], KD_LO, KD_HI))])
            xr = np.array([round(x[0], 1), round(x[1], 2)])           # what the VFD can be commanded to
            er = ev(xr)
            if all(er[k] >= LIMITS["margin"] - 1e-9 if k == "margin_raw" else True for k in ("margin_raw",)) and (
                er["fill"] >= LIMITS["fill"] and er["goodman"] <= LIMITS["goodman"] and er["torque"] <= LIMITS["torque"]
                    and er["margin_raw"] >= LIMITS["margin"] and er["objective"] > best_e["objective"]):
                best_x, best_e = xr, er
        except Exception:  # pragma: no cover - keep the grid optimum
            pass
    return {"spm": float(best_x[0]), "kd": float(best_x[1]), "eval": best_e, "feasible": ok}


def _kwh_per_bbl(e) -> float:
    return float(e["kw"] * 24 / max(float(e["oil"]), 0.5))


def recommend(steam: float, cycle_day: float, spm: float, kd: float, well: dict | None = None, price_oil: float = PRICE["oil"],
              risk_model=None, refine: bool = True) -> dict[str, Any]:
    """Pump recommendation for the current twin state, same shape as ``WellSim.metrics().recommendation`` plus hz/impacts."""
    w = {**DEFAULT_WELL, **(well or {})}
    if cycle_day < SOAK_END:
        joint_spm = float(np.clip(spm, 2, 9))
        return {"title": "Hold: steaming" if cycle_day < 14 else "Hold: soak",
                "detail": f"Pre-set production at {joint_spm:.1f} SPM once the unit restarts.", "spm": joint_spm, "kd": kd,
                "hz": joint_spm * 50 / 9, "stroke": S_M, "deltas": {"oil": 0.0, "float": 0.0, "energy": 0.0, "impacts": 0.0},
                "confidence": 0.7, "feasible": True, "model": ID, "source": "physics_synthetic"}
    t0 = time.perf_counter()
    bs = base_state(steam, cycle_day, w)
    t_prod = cycle_day - SOAK_END
    cur = evaluate(bs, w, np.array(float(spm)), np.array(float(kd)), t_prod, price_oil)
    cur = {k: float(np.asarray(v)) for k, v in cur.items() if np.size(v) == 1}       # type: ignore[misc]
    opt = optimise_point(bs, w, t_prod, price_oil, refine)
    e = opt["eval"]
    d_oil = (e["oil"] - cur["oil"]) / max(cur["oil"], 0.5)
    d_float = float(np.clip(e["margin_raw"], -1, 1) - np.clip(cur["margin_raw"], -1, 1))
    d_energy = (_kwh_per_bbl(e) - _kwh_per_bbl(cur)) / max(_kwh_per_bbl(cur), 0.1)
    d_imp = (e["impacts"] - cur["impacts"]) / max(cur["impacts"], 1.0)
    same = abs(opt["spm"] - spm) < 0.15 and abs(opt["kd"] - kd) < 0.015
    if same:
        title, detail = "Hold settings", "Pump, rods and reservoir are balanced."
    elif cur["margin_raw"] < LIMITS["margin"] + 0.05 or cur["goodman"] > LIMITS["goodman"]:
        title = "Slow down and shape the stroke"
        detail = (f"Rods are near float (margin {cur['margin_raw'] * 100:.0f}%). Run {opt['spm']:.1f} SPM with kd {opt['kd']:.2f} to restore margin.")
    elif cur["fill"] < LIMITS["fill"] + 0.03:
        title = "Match pump speed to inflow"
        detail = (f"Fillage {cur['fill'] * 100:.0f}%: the pump outruns the reservoir. Run {opt['spm']:.1f} SPM (kd {opt['kd']:.2f}) "
                  f"to cut fluid pound ({d_imp * 100:+.0f}% impacts) and power.")
    else:
        title = "Tune pump speed and stroke shape"
        detail = f"Run {opt['spm']:.1f} SPM with kd {opt['kd']:.2f}: {d_oil * 100:+.1f}% oil, {d_imp * 100:+.0f}% impacts, {d_energy * 100:+.0f}% kWh/bbl."
    slack = min((e["margin_raw"] - LIMITS["margin"]) / 0.3, (e["fill"] - LIMITS["fill"]) / 0.15, (LIMITS["goodman"] - e["goodman"]) / 0.3,
                (LIMITS["torque"] - e["torque"]) / 0.3)
    conf = float(np.clip(0.72 + 0.2 * min(max(slack, 0), 1), 0.5, 0.95)) if opt["feasible"] else 0.5
    out: dict[str, Any] = {
        "title": title, "detail": detail, "spm": round(opt["spm"], 2), "kd": round(opt["kd"], 3), "hz": opt["spm"] * 50 / 9,
        "stroke": S_M, "deltas": {"oil": float(d_oil), "float": d_float, "energy": float(d_energy), "impacts": float(d_imp)},
        "confidence": conf, "feasible": bool(opt["feasible"]),
        "impacts_per_day": {"now": cur["impacts"], "recommended": e["impacts"]},
        "constraints": {k: float(e[k]) for k in ("margin_raw", "fill", "goodman", "torque")},
        "objective_inr_per_day": {"now": cur["objective"], "recommended": e["objective"]},
        "oil_bpd": {"now": cur["oil"], "recommended": e["oil"]}, "model": ID, "source": "physics_synthetic",
        "latency_ms": (time.perf_counter() - t0) * 1000,
    }
    if risk_model is not None:                      # M4 30-day risk before/after (informational)
        from .m4_risk import cov_from_settings

        try:
            for name, (s_, k_) in (("now", (spm, kd)), ("recommended", (opt["spm"], opt["kd"]))):
                cv = cov_from_settings(w | {"stress_factor": w["rod_stress_factor"]}, steam, s_, k_)
                out.setdefault("risk_30d", {})[name] = risk_model.assess(cv, max(t_prod, 1.0))["risk_30d"]
        except Exception:  # pragma: no cover
            pass
    return out


def plan_pump(steam: float, well: dict, soak_days: float = 4.0, cutoff_twin: int = 110, price_oil: float = PRICE["oil"],
              spm_grid=SPM_GRID, kd_grid=KD_GRID) -> dict[str, Any]:
    """Best constant (spm, kd) for a whole production period (the nested inner problem of O2): grid over spm x kd x days,
    constraint = min float margin over the period >= 0.15 and mean-fill/Goodman/torque limits on peak days."""
    w = {**DEFAULT_WELL, **well}
    b = ft.base_at(ft.eff_steam(steam, float(w["steam_eff"])))
    sl = slice(SOAK_END, int(cutoff_twin) + 1)
    f = {n: ft.base_field(b, n)[sl][None, None, :] for n in ("qIn", "wc", "c", "c500", "c800", "muPump")}
    S = spm_grid[:, None, None]
    K = kd_grid[None, :, None]
    r = ft.core(f["qIn"] * float(w["pi_factor"]), f["wc"], f["c"], f["c500"], f["c800"], S, K)
    value = (r["oil"] * price_oil - r["kw"] * 24 * PRICE["kwh"]).sum(-1)
    oil = r["oil"].sum(-1)
    imp = (m5_stroke.impacts_per_day(S, r["fill"])).mean(-1)
    # risk over the period (rod + unseat expected job cost), coarse: mean over days
    ivel = m5_stroke.impact_velocity(S, r["fill"])
    uplift = pump_uplift_kn(f["muPump"] * float(w["visc_factor"]), np.pi * S_M * S / 60, r["fill"], ivel)
    un = 1 - np.exp(-pump_unseat_hazard(uplift, float(w["hold_down_kn"])).sum(-1))       # P(at least one unseat)
    gm = r["goodman"].mean(-1)
    rod_rate = rod_damage_rate(rod_shape()[None, None, :] * gm[..., None] * float(w["rod_stress_factor"]), S[..., 0][..., None] * 1440, 0.0,
                               imp[..., None], ivel.mean(-1)[..., None], float(w["corrosion_index"]))
    T = float(len(range(SOAK_END, int(cutoff_twin) + 1)))
    rod_fail = np.sum(1 - np.exp(-((rod_rate * T) ** WEIBULL_K)), axis=-1)               # expected rod parts (P per rod)
    risk = rod_fail * C_ROD + un * C_UNSEAT
    obj = value - risk
    feas = (r["margin_raw"].min(-1) >= MARGIN_REQ) & (r["goodman"].max(-1) <= LIMITS["goodman"]) & (r["torque"].max(-1) <= 1.0)
    score = np.where(feas, obj, -np.inf)
    if feas.any():
        i, j = np.unravel_index(int(np.argmax(score)), score.shape)
        ok = True
    else:
        viol = np.maximum(0, MARGIN_REQ - r["margin_raw"].min(-1))
        i, j = np.unravel_index(int(np.argmin(viol)), viol.shape)
        ok = False
    return {"spm": float(spm_grid[i]), "kd": float(kd_grid[j]), "value": float(value[i, j]), "risk_cost": float(risk[i, j]),
            "objective": float(obj[i, j]), "oil": float(oil[i, j]), "impacts_day": float(imp[i, j]),
            "min_margin": float(r["margin_raw"].min(-1)[i, j]), "feasible": bool(ok)}


def sample_states(n: int, seed: int = 11) -> list[dict]:
    """Operating states resembling S2: steam, cycle day and the operator's current spm/kd."""
    r = np.random.default_rng([common.SEED, seed])
    return [{"steam": float(r.uniform(500, 1200)), "cycle_day": float(r.uniform(22, 112)), "spm": float(r.uniform(4.0, 7.2)),
             "kd": float(r.choice([0.46, 0.5, 0.54, 0.58, 0.62])),
             "well": {"pi_factor": float(r.uniform(0.7, 1.3)), "visc_factor": float(np.exp(r.normal(0, 0.15))),
                      "steam_eff": float(r.uniform(0.9, 1.1)), "rod_stress_factor": float(r.uniform(1.15, 1.6)),
                      "corrosion_index": float(r.uniform(0.1, 0.8)), "hold_down_kn": float(r.uniform(22, 30))}} for _ in range(n)]


def train(out_dir: Path, quick: bool = False) -> dict:
    """O1 has no learned weights: 'training' validates against the baseline on sampled states and writes the config."""
    with common.timer() as tm:
        ft.tables()
        n = 40 if quick else 400
        st = sample_states(n)
        imp0 = imp1 = oil0 = oil1 = obj0 = obj1 = 0.0
        viol_now = viol_new = feas = 0
        lat = []
        pairs = []
        for s in st:
            rec = recommend(s["steam"], s["cycle_day"], s["spm"], s["kd"], s["well"])
            lat.append(rec["latency_ms"])
            w = {**DEFAULT_WELL, **s["well"]}
            bs = base_state(s["steam"], s["cycle_day"], w)
            cur = evaluate(bs, w, np.array(s["spm"]), np.array(s["kd"]), s["cycle_day"] - SOAK_END)
            imp0 += float(cur["impacts"])
            imp1 += rec["impacts_per_day"]["recommended"]
            oil0 += float(cur["oil"])
            oil1 += rec["oil_bpd"]["recommended"]
            obj0 += float(cur["objective"])
            obj1 += rec["objective_inr_per_day"]["recommended"]
            viol_now += int(not bool(_feasible(cur)))
            viol_new += int(not rec["feasible"])
            feas += int(rec["feasible"])
            pairs.append((float(cur["impacts"]), rec["impacts_per_day"]["recommended"], float(cur["oil"]), rec["oil_bpd"]["recommended"]))
        # states where the operator's setting causes pounding (baseline impacts > 500/day): the ones the controller targets
        pd_ = [p for p in pairs if p[0] > 500]
        red_pound = 1 - sum(p[1] for p in pd_) / max(sum(p[0] for p in pd_), 1e-9) if pd_ else 0.0
        oil_pound = sum(p[3] for p in pd_) / max(sum(p[2] for p in pd_), 1e-9) - 1 if pd_ else 0.0
        met = {"impacts_reduction_all_states": 1 - imp1 / max(imp0, 1e-9), "oil_change_all_states": oil1 / max(oil0, 1e-9) - 1,
               "impacts_reduction_pounding_states": red_pound, "oil_change_pounding_states": oil_pound,
               "n_pounding_states": len(pd_), "objective_gain_inr_per_day_mean": (obj1 - obj0) / n,
               "baseline_infeasible_share": viol_now / n, "recommended_infeasible_share": viol_new / n,
               "latency_ms_p50": float(np.percentile(lat, 50)), "latency_ms_p95": float(np.percentile(lat, 95)), "n_states": n}
    d = common.model_dir(ID, out_dir)
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "limits": LIMITS,
            "trained_at": common.now_iso(), "data_hash": common.data_hash([str(LIMITS), str(n)])}
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "impacts_reduction_all_states", "value": met["impacts_reduction_all_states"], "target": 0.15,
                                     "baseline_name": "fixed_spm (0 % by definition)", "baseline": 0.0, "direction": "higher",
                                     "secondary": {"name": "oil_change_all_states", "value": met["oil_change_all_states"], "target": -0.02}},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"], "data_hash": meta["data_hash"],
          "quick": quick}
    card = f"""# O1 SRP controller
Constrained optimisation of pump speed and stroke shape (kd) on the physics twin: maximise oil value - energy cost - risk cost subject to
float margin >= 0.15, fillage >= 0.8, Goodman <= 0.9, torque <= 1.0 (grid warm start + SLSQP; tabulated twin core, ~ms per call).
**Source: physics_synthetic** (the twin itself; no learned weights, so `train` = validation on {n} sampled states drawn like S2).
- Output: title, detail, spm, kd, hz, stroke, deltas{{oil, float, energy, impacts}}, confidence (+ constraints, impacts/day, objective).
- Metrics vs today's fixed SPM: {json.dumps(met)}. Target: >= 15 % fewer impacts at <= 2 % oil loss.
- Risk cost uses the physics hazard laws (same as S5/M4); stroke-hole selection is not modelled (the twin has one stroke length).
- Limits: optimum is for the current cycle day (myopic); fillage >= 0.8 makes the controller slow the unit whenever inflow is the bottleneck.
"""
    return common.write_eval(d, ID, ev, card)
