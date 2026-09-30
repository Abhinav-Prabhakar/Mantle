"""O2 CSS planner: Optuna TPE over (steam t, injection pressure, soak d, cut-off d) on the M1/M2 surrogates.

* **Joint**: every candidate plan is scored with the O1 pump optimum nested inside (``o1_srp.plan_pump``).
* **Sequential** (today's workflow): steam plan chosen at a today's pump (5.4 SPM, kd 0.5), then the pump re-optimised.
* **Coupling dividend** = value(joint) - value(sequential), INR per cycle, on the same evaluator. The joint study is seeded
  with the sequential plan, so joint >= sequential by construction.
* Practice baseline (backend.md L13 / UI fixture): 800 t, 9.0 MPa, 4 d soak, 120 d cut-off at 5.4 SPM / kd 0.5.
Oil comes from M2 (P10/P90 conformal), energy/float/Goodman from the tabulated twin, risk cost from the physics hazard.
Injection pressure is a modelling assumption: the twin has no pressure physics, so the required pressure follows the S2
relation p_req = 7 + (steam-500)/140 MPa; excess pressure is penalised as boiler fuel and a shortfall as lost injectivity.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import optuna

from mantle_physics.constants import BBL_PER_T_CWE, INJ_END, PRICE, SOAK_END

from .. import common
from .. import fasttwin as ft
from . import m2_forecast as m2
from . import o1_srp

ID = "O2"
RANGES = {"steam": [500, 1200], "pInj": [7, 12], "soak": [2, 10], "cutoff": [40, 120]}
PRACTICE = {"steam": 800.0, "pInj": 9.0, "soak": 4.0, "cutoff": 120.0}
PRACTICE_PUMP = (5.4, 0.5)
NOMINAL_PUMP = PRACTICE_PUMP           # steam is planned around today's pump settings
P_EXCESS_INR_PER_MPA_T = 30.0        # boiler fuel for pressure above the injectivity requirement (per tonne of steam)
P_SHORT_INR_PER_MPA_T = 250.0        # lost injectivity below it


def p_required(steam: float) -> float:
    return 7.0 + (steam - 500.0) / 140.0


class Planner:
    def __init__(self, forecaster: m2.ForecastModel):
        self.m2 = forecaster
        self._cache: dict[str, dict] = {}

    # ------------------------------------------------------------ evaluation
    def _pump(self, well: dict, plan: dict, fixed: tuple[float, float] | None) -> dict:
        cut_twin = int(min(120, round(plan["cutoff"])))
        kw = {"steam": plan["steam"], "well": well, "soak_days": plan["soak"], "cutoff_twin": cut_twin}
        if fixed is not None:
            return o1_srp.plan_pump(**kw, spm_grid=np.array([fixed[0]]), kd_grid=np.array([fixed[1]]))
        return o1_srp.plan_pump(**kw)

    def value(self, well: dict, plan: dict, pump: dict, cycle_no: int, scale: float = 1.0) -> dict:
        """Surrogate value (INR/cycle) of a plan at a pump policy, with M2 P10/P90."""
        cut_actual = int(round(plan["cutoff"] + plan["soak"] - 4))
        f = self.m2.predict_daily(well, plan["steam"], plan["soak"], pump["spm"], pump["kd"], cut_actual, cycle_no, plan["pInj"],
                                  scale=scale)
        cum = float(f["cum_oil"])
        b = ft.base_at(ft.eff_steam(plan["steam"], float(well["steam_eff"])))
        d0, d1 = SOAK_END, int(min(120, round(plan["cutoff"])))
        sl = slice(d0, d1 + 1)
        r = ft.core(ft.base_field(b, "qIn")[sl] * float(well["pi_factor"]), ft.base_field(b, "wc")[sl], ft.base_field(b, "c")[sl],
                    ft.base_field(b, "c500")[sl], ft.base_field(b, "c800")[sl], pump["spm"], pump["kd"])
        energy = float(np.sum(r["kw"]) * 24 * PRICE["kwh"])
        steam_cost = plan["steam"] * PRICE["steamT"]
        p_req = p_required(plan["steam"])
        press = plan["steam"] * (P_EXCESS_INR_PER_MPA_T * max(0.0, plan["pInj"] - p_req)
                                 + P_SHORT_INR_PER_MPA_T * max(0.0, p_req - 0.3 - plan["pInj"]))
        fixed_costs = energy + steam_cost + press + pump["risk_cost"]
        penalty = 0.0 if pump["feasible"] else 3.0e5
        val = cum * PRICE["oil"] - fixed_costs - penalty
        return {"value": val, "value_p10": float(f["cum_p10"]) * PRICE["oil"] - fixed_costs - penalty,
                "value_p90": float(f["cum_p90"]) * PRICE["oil"] - fixed_costs - penalty, "cum_oil": cum,
                "cum_p10": float(f["cum_p10"]), "cum_p90": float(f["cum_p90"]), "sor": steam_sor(plan["steam"], cum),
                "energy_inr": energy, "steam_inr": steam_cost, "risk_inr": pump["risk_cost"], "forecast": f}

    def score(self, well: dict, plan: dict, cycle_no: int, fixed_pump: tuple[float, float] | None, scale: float = 1.0) -> dict:
        pump = self._pump(well, plan, fixed_pump)
        v = self.value(well, plan, pump, cycle_no, scale)
        v["pump"] = pump
        return v

    # ------------------------------------------------------------ search
    def _study(self, well, cycle_no, fixed_pump, n_trials, timeout, seed, scale, enqueue=None, stop_at: float | None = None):
        sampler = optuna.samplers.TPESampler(seed=seed, n_startup_trials=min(25, n_trials // 3), multivariate=True)
        study = optuna.create_study(direction="maximize", sampler=sampler)
        optuna.logging.set_verbosity(optuna.logging.ERROR)
        if enqueue:
            study.enqueue_trial(enqueue)
        cache: dict[tuple, float] = {}

        def objective(t: optuna.Trial) -> float:
            steam = t.suggest_int("steam", RANGES["steam"][0], RANGES["steam"][1], step=10)
            plan = {"steam": float(steam), "pInj": round(t.suggest_float("pInj", *RANGES["pInj"]), 2),
                    "soak": float(t.suggest_int("soak", *RANGES["soak"])), "cutoff": float(t.suggest_int("cutoff", *RANGES["cutoff"], step=2))}
            key = (plan["steam"], plan["pInj"], plan["soak"], plan["cutoff"])
            if key not in cache:
                cache[key] = self.score(well, plan, cycle_no, fixed_pump, scale)["value"]
            return cache[key]

        study.optimize(objective, n_trials=n_trials, timeout=timeout)
        bp = study.best_params
        best = {"steam": float(bp["steam"]), "pInj": round(float(bp["pInj"]), 2), "soak": float(bp["soak"]), "cutoff": float(bp["cutoff"])}
        return best, len(study.trials)

    def plan(self, well: dict, cycle_no: int | None = None, history: list[tuple[float, float]] | None = None,
             budget_s: float = 5.0, seed: int = 0, use_cache: bool = True) -> dict[str, Any]:
        """Plan the next cycle for ``well`` (a row of the wells table). ``history`` = [(predicted, actual) cum oil] of earlier
        cycles for the per-well Bayesian scaling. Results are cached per (well, cycle, history, seed)."""
        cyc = int(cycle_no or 1)
        key = hashlib.sha1(json.dumps([well.get("well_id"), cyc, history, seed, round(budget_s, 1)]).encode()).hexdigest()[:16]
        if use_cache and key in self._cache:
            return self._cache[key]
        t0 = time.perf_counter()
        scale = m2.well_scale(history or [])
        ft.tables()
        # sequential: steam plan at nominal pump (35 % of budget), then re-optimise the pump on that plan
        n_seq, n_joint = (60, 110) if budget_s >= 3 else (12, 20)
        seq_plan, n1 = self._study(well, cyc, NOMINAL_PUMP, n_seq, 0.35 * budget_s, seed, scale)
        seq = self.score(well, seq_plan, cyc, None, scale)
        # joint: all four levers with the pump nested; seeded with the sequential plan (=> joint >= sequential)
        remaining = max(0.5, budget_s - (time.perf_counter() - t0))
        enq = {"steam": int(seq_plan["steam"]), "pInj": seq_plan["pInj"], "soak": int(seq_plan["soak"]), "cutoff": int(seq_plan["cutoff"])}
        joint_plan, n2 = self._study(well, cyc, None, n_joint, remaining, seed + 1, scale, enqueue=enq)
        joint = self.score(well, joint_plan, cyc, None, scale)
        if joint["value"] < seq["value"]:
            joint_plan, joint = seq_plan, seq
        practice_pump = {"spm": PRACTICE_PUMP[0], "kd": PRACTICE_PUMP[1]}
        pr = self.score(well, PRACTICE, cyc, PRACTICE_PUMP, scale)
        dividend = max(0.0, joint["value"] - seq["value"])
        gain = joint["value"] - pr["value"]
        out = {
            "well_id": well.get("well_id"), "cycle_no": cyc,
            "practice": dict(PRACTICE), "mantle": {k: joint_plan[k] for k in ("steam", "pInj", "soak", "cutoff")},
            "ranges": RANGES,
            "pump": {"spm": joint["pump"]["spm"], "kd": joint["pump"]["kd"], "practice_spm": practice_pump["spm"],
                     "practice_kd": practice_pump["kd"]},
            "oil_lift": joint["cum_oil"] / max(pr["cum_oil"], 1.0) - 1.0,
            "sor": [pr["sor"], joint["sor"]],
            "inr_per_cycle": gain, "joint_share": dividend,
            "coupling_dividend_inr": dividend,
            "sequential": {"plan": seq_plan, "pump": {"spm": seq["pump"]["spm"], "kd": seq["pump"]["kd"]}, "value_inr": seq["value"],
                           "oil_bbl": seq["cum_oil"]},
            "joint": {"value_inr": joint["value"], "oil_bbl": joint["cum_oil"], "cum_oil_p10": joint["cum_p10"],
                      "cum_oil_p90": joint["cum_p90"]},
            "practice_value_inr": pr["value"], "practice_oil_bbl": pr["cum_oil"],
            "p10_p90": {"inr_per_cycle": [joint["value_p10"] - pr["value"], joint["value_p90"] - pr["value"]],
                        "oil_lift": [joint["cum_p10"] / max(pr["cum_oil"], 1.0) - 1.0, joint["cum_p90"] / max(pr["cum_oil"], 1.0) - 1.0]},
            "plan_curve": {"day": joint["forecast"]["day"].tolist(), "oil": joint["forecast"]["oil"].tolist(),
                           "oil_p10": joint["forecast"]["oil_p10"].tolist(), "oil_p90": joint["forecast"]["oil_p90"].tolist()},
            "trials": {"sequential": n1, "joint": n2}, "well_scale": scale, "seconds": time.perf_counter() - t0,
            "model": ID, "source": "physics_synthetic",
        }
        self._cache[key] = out
        return out


def steam_sor(steam: float, cum_oil: float) -> float:
    return float(np.clip(steam * BBL_PER_T_CWE / max(cum_oil, 1.0), 0, 99)) if cum_oil > 5 else 0.0


def to_ui(p: dict) -> dict:
    """The UI's ``PLAN`` fixture shape (camelCase)."""
    return {"practice": p["practice"], "mantle": p["mantle"], "ranges": p["ranges"], "oilLift": p["oil_lift"], "sor": p["sor"],
            "inrPerCycle": p["inr_per_cycle"], "jointShare": p["joint_share"]}


# ---------------------------------------------------------------- training / validation


def _twin_value(well: dict, plan: dict, pump: tuple[float, float], cycle_no: int) -> tuple[float, float]:
    """Ground-truth-ish check with the S2 generating process (noiseless): value INR and cum oil."""
    from mantle_data.synth.wellmodel import cycle_run, cycle_totals

    scale = well["pi_factor"] * well["decline_rate"] ** (cycle_no - 1)
    run = cycle_run(plan["steam"], pump[0], pump[1], steam_eff=well["steam_eff"], oil_scale=scale, visc_factor=well["visc_factor"],
                    soak_days=plan["soak"])
    tot = cycle_totals(run, plan["steam"], int(min(120, plan["cutoff"])))
    return float(tot["net_inr"]), float(tot["cum_oil"])


def train(out_dir: Path, quick: bool = False) -> dict:
    """No learned weights: run the planner on wells, verify against the twin, cache plans per well."""
    from .. import data
    from . import m0_viscosity as m0
    from . import m1_thermal as m1

    root = Path(out_dir)
    for mid, mod in (("M0", m0), ("M1", __import__("mantle_ml.models.m1_thermal", fromlist=["x"])), ("M2", m2)):
        if not (root / mid / "model.joblib").exists():
            mod.train(root, quick=True)
    with common.timer() as tm:
        if quick:
            data.ensure_small_data()
        fm = m2.ForecastModel.load(root / "M2", m1.ThermalModel.load(root / "M1"), m0.ViscosityModel.load(root / "M0"))
        planner = Planner(fm)
        wells = data.wells()
        cyc = data.cycles()
        n_wells = 3 if quick else len(wells)
        budget = 1.0 if quick else 4.0
        rows, plans = [], {}
        for w in wells.head(n_wells).to_dict("records"):
            nxt = int(cyc[cyc.well_id == w["well_id"]]["cycle_no"].max() + 1) if (cyc.well_id == w["well_id"]).any() else 1
            p = planner.plan(w, nxt, budget_s=budget)
            plans[w["well_id"]] = {k: v for k, v in p.items() if k != "plan_curve"}
            tv_m, oil_m = _twin_value(w, p["mantle"], (p["pump"]["spm"], p["pump"]["kd"]), nxt)
            tv_p, oil_p = _twin_value(w, PRACTICE, PRACTICE_PUMP, nxt)
            tv_s, _ = _twin_value(w, p["sequential"]["plan"], (p["sequential"]["pump"]["spm"], p["sequential"]["pump"]["kd"]), nxt)
            rows.append({"seconds": p["seconds"], "dividend": p["coupling_dividend_inr"], "joint_ge_seq": p["joint"]["value_inr"] >= p["sequential"]["value_inr"] - 1e-6,
                         "gain": p["inr_per_cycle"], "oil_lift": p["oil_lift"], "sor_p": p["sor"][0], "sor_m": p["sor"][1],
                         "twin_gain": tv_m - tv_p, "twin_dividend": tv_m - tv_s, "twin_oil_lift": oil_m / max(oil_p, 1) - 1,
                         "in_range": all(RANGES[k][0] <= p["mantle"][k] <= RANGES[k][1] for k in RANGES)})
        R = {k: np.array([r[k] for r in rows], dtype=float) for k in rows[0]}
        met = {"n_wells": len(rows), "seconds_max": float(R["seconds"].max()), "seconds_mean": float(R["seconds"].mean()),
               "joint_ge_sequential_all": bool(R["joint_ge_seq"].all()), "ranges_valid_all": bool(R["in_range"].all()),
               "coupling_dividend_inr_mean_surrogate": float(R["dividend"].mean()),
               "gain_vs_practice_inr_mean_surrogate": float(R["gain"].mean()), "oil_lift_mean_surrogate": float(R["oil_lift"].mean()),
               "sor_practice_mean": float(R["sor_p"].mean()), "sor_mantle_mean": float(R["sor_m"].mean()),
               "gain_vs_practice_inr_mean_twin_verified": float(R["twin_gain"].mean()),
               "share_wells_twin_gain_positive": float((R["twin_gain"] > 0).mean()),
               "coupling_dividend_inr_mean_twin_verified": float(R["twin_dividend"].mean()),
               "oil_lift_mean_twin_verified": float(R["twin_oil_lift"].mean())}
    d = common.model_dir(ID, root)
    (d / "plans.json").write_text(json.dumps(_round(plans), separators=(",", ":")))
    meta = {"version": "1.0.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "trained_at": common.now_iso(),
            "data_hash": common.data_hash([str(sorted(plans))]), "budget_s": budget}
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "gain_vs_practice_inr_per_cycle_twin_verified", "value": met["gain_vs_practice_inr_mean_twin_verified"],
                                     "target": 0.0, "target_text": "> 0 (no numeric target in spec)", "baseline_name": "practice (L13)", "baseline": 0.0,
                                     "direction": "higher"},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"], "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# O2 CSS planner
Optuna TPE over steam t, injection pressure, soak d and cut-off d with the O1 pump optimum nested (joint) versus steam-first-then-pump (sequential). **Source: physics_synthetic**
(M1/M2 surrogates trained on S2; O1 physics twin). No weights: `train` runs the planner on {met["n_wells"]} wells (budget {budget:.0f} s each), verifies each plan against the
noiseless S2 generating process (`*_twin_verified`) and caches the plans in `plans.json`.
- Metrics: {json.dumps(met)}
- Coupling dividend = value(joint) - value(sequential) (INR/cycle); the joint study is seeded with the sequential plan so joint >= sequential. Output shape matches the UI PLAN fixture (`to_ui`).
- Practice baseline is the fixture (800 t, 9 MPa, 4 d, 120 d at 5.4 SPM). P10-P90 come from M2's conformal cycle interval applied to the mantle plan only.
- Limits: injection pressure is a modelling assumption (no pressure physics in the twin); the surrogate-optimal plan is checked against the twin, not against field results; cut-off is on the twin's day axis.
"""
    return common.write_eval(d, ID, ev, card)


def _round(o: Any) -> Any:
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_round(v) for v in o]
    if isinstance(o, float):
        return None if not math.isfinite(o) else round(o, 4)
    return o


_ = INJ_END
