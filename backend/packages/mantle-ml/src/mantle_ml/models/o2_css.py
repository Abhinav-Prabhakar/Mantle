"""O2 CSS planner: Optuna TPE over (steam t, injection pressure, soak d, cut-off d), scored per cycle-day on the calibrated twin.

Objective (a repeating cycle): **net value per calendar day** = (oil revenue - power - steam - pressure penalty - pump risk cost)
/ cycle length, with cycle length = injection days (steam / generator rate) + soak + production days to the cut-off. Cutting
off earlier costs oil but frees the well for the next steam job, so the cut-off, soak and steam volume all enter through the
denominator exactly as in the twin's own economic cut-off rule (``economics.days_to_cutoff``: best whole-cycle average margin).
* **Joint**: every candidate plan is scored with the O1 pump optimum nested inside (``o1_srp.plan_pump``).
* **Sequential** (today's workflow): steam plan chosen at today's pump (5.4 SPM, kd 0.5), then the pump re-optimised.
* **Coupling dividend** = value(joint) - value(sequential), on the same evaluator.
* Practice baseline (L13 / UI fixture): 800 t, 9.0 MPa, 4 d soak, 120 d cut-off at 5.4 SPM / kd 0.5.
Every reported number (oil lift, SOR pair, INR per cycle, joint share, the plan curve) is **re-run on the exact twin**
(``synth.wellmodel.cycle_run``: the scalar twin with the well's productivity / viscosity / steam-efficiency factors, the same
basis as the API's ``/state`` metrics) for the chosen joint, sequential and practice plans. M2 supplies the P10-P90 band and
is reported as a cross-check. SOR is ``economics.sor`` on the cumulative oil to each plan's cut-off. INR per cycle and oil lift
compare plans over the same calendar time (one practice cycle), because plans of different cycle length cannot be compared per cycle.
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

from mantle_physics.constants import BBL_PER_T_CWE, INJ_END, PRICE, SOAK_END, STEAM_RATE_T_PER_D
from mantle_physics.economics import sor as sor_fn

from .. import common
from .. import fasttwin as ft
from . import m2_forecast as m2
from . import o1_srp

ID = "O2"
RANGES = {"steam": [500, 1200], "pInj": [7, 12], "soak": [2, 10], "cutoff": [40, 120]}
PRACTICE = {"steam": 800.0, "pInj": 9.0, "soak": 4.0, "cutoff": 120.0}
PRACTICE_PUMP = (5.4, 0.5)
NOMINAL_PUMP = PRACTICE_PUMP           # steam is planned around today's pump settings
STEAM_STEP = 0.25                      # operational trust region: steam volume within +-25 % of the practice volume (thermal-battery continuity,
                                       # and the surrogates are trained around it); the twin's per-day optimum is flat and sits near the 500 t bound
STEAM_TRUST = (max(RANGES["steam"][0], PRACTICE["steam"] * (1 - STEAM_STEP)), min(RANGES["steam"][1], PRACTICE["steam"] * (1 + STEAM_STEP)))
P_EXCESS_INR_PER_MPA_T = 30.0        # boiler fuel for pressure above the injectivity requirement (per tonne of steam)
P_SHORT_INR_PER_MPA_T = 250.0        # lost injectivity below it
INFEASIBLE_PENALTY_INR = 3.0e5


def p_required(steam: float) -> float:
    return 7.0 + (steam - 500.0) / 140.0


def cycle_days(plan: dict) -> float:
    """Calendar length of one cycle: inject the steam, soak, then produce from twin day 18 to the cut-off."""
    return float(plan["steam"]) / STEAM_RATE_T_PER_D + float(plan["soak"]) + (float(plan["cutoff"]) - SOAK_END)


def _extra_costs(plan: dict, pump: dict) -> float:
    p_req = p_required(plan["steam"])
    press = plan["steam"] * (P_EXCESS_INR_PER_MPA_T * max(0.0, plan["pInj"] - p_req)
                             + P_SHORT_INR_PER_MPA_T * max(0.0, p_req - 0.3 - plan["pInj"]))
    return press + pump["risk_cost"] + (0.0 if pump["feasible"] else INFEASIBLE_PENALTY_INR)


def _twin_arrays(well: dict, plan: dict, pump: dict, exact: bool) -> tuple[np.ndarray, np.ndarray]:
    """(oil bpd, motor kW) over twin days 0..120. ``exact``: the scalar twin; else the tabulated copy used inside the search."""
    from mantle_data.synth.wellmodel import cycle_run, soak_factor

    if exact:
        r = cycle_run(plan["steam"], pump["spm"], pump["kd"], steam_eff=float(well["steam_eff"]), oil_scale=float(well["pi_factor"]),
                      visc_factor=float(well["visc_factor"]), soak_days=plan["soak"])
        return r.oil, r.kw
    k = float(well["pi_factor"]) * soak_factor(plan["soak"])
    r2 = ft.cycle_days(plan["steam"], pump["spm"], pump["kd"], steam_eff=float(well["steam_eff"]), k_oil=k)
    return r2["oil"], r2["kw"]


def twin_value(well: dict, plan: dict, pump: dict, exact: bool = True) -> dict:
    """One cycle of ``plan`` at ``pump`` on the twin: cumulative oil to the cut-off, INR per cycle and per calendar day, SOR."""
    oil, kw = _twin_arrays(well, plan, pump, exact)
    cut = int(min(120, round(plan["cutoff"])))
    sl = slice(SOAK_END, cut + 1)
    cum = float(np.trapezoid(oil[sl]))
    energy = float(np.trapezoid(kw[sl]) * 24 * PRICE["kwh"])
    steam_inr = plan["steam"] * PRICE["steamT"]
    extra = _extra_costs(plan, pump)
    value = cum * PRICE["oil"] - energy - steam_inr - extra
    days = cycle_days({**plan, "cutoff": cut})
    return {"value": value, "days": days, "rate": value / days, "cum_oil": cum, "oil_per_day": cum / days, "energy_inr": energy,
            "steam_inr": steam_inr, "risk_inr": pump["risk_cost"], "sor": float(sor_fn(plan["steam"], cum)),
            "oil": oil, "kw": kw, "cutoff": cut}


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

    def score(self, well: dict, plan: dict, fixed_pump: tuple[float, float] | None, exact: bool = False) -> dict:
        pump = self._pump(well, plan, fixed_pump)
        v = twin_value(well, plan, pump, exact)
        v["pump"] = pump
        return v

    def m2_check(self, well: dict, plan: dict, pump: dict, cycle_no: int, scale: float = 1.0) -> dict:
        """M2 forecast of the plan: cumulative oil with P10/P90 (cross-check and uncertainty band)."""
        cut_actual = int(round(plan["cutoff"] + plan["soak"] - 4))
        return self.m2.predict_daily(well, plan["steam"], plan["soak"], pump["spm"], pump["kd"], cut_actual, cycle_no, plan["pInj"],
                                     scale=scale)

    # ------------------------------------------------------------ search
    def _study(self, well, fixed_pump, n_trials, timeout, seed, enqueue=None):
        sampler = optuna.samplers.TPESampler(seed=seed, n_startup_trials=min(25, n_trials // 3), multivariate=True)
        study = optuna.create_study(direction="maximize", sampler=sampler)
        optuna.logging.set_verbosity(optuna.logging.ERROR)
        for e in enqueue or []:
            study.enqueue_trial(e)
        cache: dict[tuple, float] = {}

        def objective(t: optuna.Trial) -> float:
            steam = t.suggest_int("steam", int(STEAM_TRUST[0]), int(STEAM_TRUST[1]), step=10)
            plan = {"steam": float(steam), "pInj": round(t.suggest_float("pInj", *RANGES["pInj"]), 2),
                    "soak": float(t.suggest_int("soak", *RANGES["soak"])), "cutoff": float(t.suggest_int("cutoff", *RANGES["cutoff"], step=2))}
            key = (plan["steam"], plan["pInj"], plan["soak"], plan["cutoff"])
            if key not in cache:
                cache[key] = self.score(well, plan, fixed_pump)["rate"]
            return cache[key]

        study.optimize(objective, n_trials=n_trials, timeout=timeout)
        bp = study.best_params
        best = {"steam": float(bp["steam"]), "pInj": round(float(bp["pInj"]), 2), "soak": float(bp["soak"]), "cutoff": float(bp["cutoff"])}
        return best, len(study.trials)

    def _polish(self, well: dict, plan: dict, fixed_pump: tuple[float, float] | None) -> dict:
        """Coordinate sweep of the two levers TPE resolves worst, cut-off and soak (a few ms per point, exact grid)."""
        best, best_v = dict(plan), self.score(well, plan, fixed_pump)["rate"]
        for _ in range(2):
            for key, grid in (("cutoff", range(RANGES["cutoff"][0], RANGES["cutoff"][1] + 1, 2)),
                              ("soak", range(RANGES["soak"][0], RANGES["soak"][1] + 1))):
                for x in grid:
                    cand = {**best, key: float(x)}
                    v = self.score(well, cand, fixed_pump)["rate"]
                    if v > best_v + 1e-9:
                        best, best_v = cand, v
        return best

    def plan(self, well: dict, cycle_no: int | None = None, history: list[tuple[float, float]] | None = None,
             budget_s: float = 5.0, seed: int = 0, use_cache: bool = True) -> dict[str, Any]:
        """Plan the next cycle for ``well`` (a row of the wells table). ``history`` = [(predicted, actual) cum oil] of earlier
        cycles for the per-well Bayesian scaling of the M2 band. Results are cached per (well, cycle, history, seed)."""
        cyc = int(cycle_no or 1)
        key = hashlib.sha1(json.dumps([well.get("well_id"), cyc, history, seed, round(budget_s, 1)]).encode()).hexdigest()[:16]
        if use_cache and key in self._cache:
            return self._cache[key]
        t0 = time.perf_counter()
        scale = m2.well_scale(history or [])
        ft.tables()
        n_seq, n_joint = (60, 110) if budget_s >= 3 else (12, 20)
        # sequential: steam plan at the nominal pump (35 % of budget), then re-optimise the pump on that plan
        seq_plan, n1 = self._study(well, NOMINAL_PUMP, n_seq, 0.35 * budget_s, seed,
                                   enqueue=[{"steam": 800, "pInj": 9.0, "soak": 4, "cutoff": 120}])
        seq_plan = self._polish(well, seq_plan, NOMINAL_PUMP)
        # joint: all four levers with the pump nested; seeded with the sequential plan
        remaining = max(0.5, budget_s - (time.perf_counter() - t0))
        enq = {"steam": int(seq_plan["steam"]), "pInj": seq_plan["pInj"], "soak": int(seq_plan["soak"]), "cutoff": int(seq_plan["cutoff"])}
        joint_plan, n2 = self._study(well, None, n_joint, remaining, seed + 1, enqueue=[enq])
        joint_plan = self._polish(well, joint_plan, None)
        # re-run practice / sequential / joint on the exact twin; the workflows cannot do worse than what they start from
        pr = self.score(well, PRACTICE, PRACTICE_PUMP, exact=True)
        seq = self.score(well, seq_plan, None, exact=True)
        fell_back = seq["rate"] < pr["rate"]
        if fell_back:
            seq_plan, seq = dict(PRACTICE), pr
        joint = self.score(well, joint_plan, None, exact=True)
        if joint["rate"] < seq["rate"]:
            joint_plan, joint = seq_plan, seq
        t_p = pr["days"]                                           # compare over the same calendar time: one practice cycle
        gain = (joint["rate"] - pr["rate"]) * t_p
        dividend = max(0.0, (joint["rate"] - seq["rate"]) * t_p)
        # M2 cross-check and P10-P90 band (ratios applied to the twin numbers)
        f = self.m2_check(well, joint_plan, joint["pump"], cyc, scale)
        fp = self.m2_check(well, PRACTICE, pr["pump"], cyc, scale)
        r_lo, r_hi = float(f["cum_p10"] / max(f["cum_oil"], 1e-9)), float(f["cum_p90"] / max(f["cum_oil"], 1e-9))
        rate_at = lambda r: (joint["value"] - (1 - r) * joint["cum_oil"] * PRICE["oil"]) / joint["days"]   # noqa: E731
        cut = joint["cutoff"]
        days_tw = np.arange(SOAK_END, cut + 1)
        oil_tw = joint["oil"][SOAK_END: cut + 1]
        okm = f["oil"] > 1e-9
        ratio10 = np.where(okm, f["oil_p10"] / np.where(okm, f["oil"], 1.0), r_lo)
        ratio90 = np.where(okm, f["oil_p90"] / np.where(okm, f["oil"], 1.0), r_hi)
        n = min(len(days_tw), len(ratio10))
        pc_day, pc_oil = days_tw[:n], oil_tw[:n]
        oil_pd = lambda v: v["cum_oil"] / v["days"]   # noqa: E731
        out = {
            "well_id": well.get("well_id"), "cycle_no": cyc,
            "practice": dict(PRACTICE), "mantle": {k: joint_plan[k] for k in ("steam", "pInj", "soak", "cutoff")},
            "ranges": RANGES,
            "pump": {"spm": joint["pump"]["spm"], "kd": joint["pump"]["kd"], "practice_spm": PRACTICE_PUMP[0],
                     "practice_kd": PRACTICE_PUMP[1]},
            "oil_lift": oil_pd(joint) / max(oil_pd(pr), 1e-9) - 1.0,
            "sor": [pr["sor"], joint["sor"]],
            "inr_per_cycle": gain, "joint_share": dividend,
            "coupling_dividend_inr": dividend,
            "basis": {"objective": "net value per calendar day of a repeating cycle", "evaluator": "twin (exact scalar core, well factors)",
                      "inr_per_cycle_horizon_days": t_p,
                      "sor": "economics.sor(steam, cumulative oil to the plan's cut-off) - the twin's sor metric at the cut-off day",
                      "steam_trust_region": list(STEAM_TRUST)},
            "per_cycle": {"practice_days": pr["days"], "mantle_days": joint["days"], "practice_oil_bbl": pr["cum_oil"],
                      "mantle_oil_bbl": joint["cum_oil"], "practice_inr_per_day": pr["rate"], "mantle_inr_per_day": joint["rate"],
                      "mantle_cutoff_twin_day": cut},
            "sequential": {"plan": seq_plan, "pump": {"spm": seq["pump"]["spm"], "kd": seq["pump"]["kd"]}, "value_inr": seq["value"],
                           "inr_per_day": seq["rate"], "oil_bbl": seq["cum_oil"], "fell_back_to_practice": bool(fell_back)},
            "joint": {"value_inr": joint["value"], "inr_per_day": joint["rate"], "oil_bbl": joint["cum_oil"],
                      "cum_oil_p10": joint["cum_oil"] * r_lo, "cum_oil_p90": joint["cum_oil"] * r_hi},
            "practice_value_inr": pr["value"], "practice_oil_bbl": pr["cum_oil"],
            "m2_check": {"joint_cum_oil_bbl": f["cum_oil"], "practice_cum_oil_bbl": fp["cum_oil"],
                         "joint_vs_twin": f["cum_oil"] / max(joint["cum_oil"], 1e-9) - 1.0},
            "p10_p90": {"inr_per_cycle": [(rate_at(r_lo) - pr["rate"]) * t_p, (rate_at(r_hi) - pr["rate"]) * t_p],
                        "oil_lift": [joint["cum_oil"] * r_lo / joint["days"] / max(oil_pd(pr), 1e-9) - 1.0,
                                     joint["cum_oil"] * r_hi / joint["days"] / max(oil_pd(pr), 1e-9) - 1.0]},
            "plan_curve": {"day": pc_day.tolist(), "oil": pc_oil.tolist(), "oil_p10": (pc_oil * ratio10[:n]).tolist(),
                           "oil_p90": (pc_oil * ratio90[:n]).tolist(), "cutoff": cut},
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


def _economic_cutoff(well: dict, plan: dict, pump: tuple[float, float]) -> int:
    """The twin's own cut-off rule (``economics.days_to_cutoff``) for this plan and pump, on the well's calibrated twin."""
    from mantle_data.synth.wellmodel import best_cutoff, cycle_run

    run = cycle_run(plan["steam"], pump[0], pump[1], steam_eff=float(well["steam_eff"]), oil_scale=float(well["pi_factor"]),
                    visc_factor=float(well["visc_factor"]), soak_days=plan["soak"])
    return int(best_cutoff(run, plan["steam"], lo=SOAK_END + 1))


def train(out_dir: Path, quick: bool = False) -> dict:
    """No learned weights: run the planner on wells, re-check each plan on the exact twin, cache plans (with curves) per well."""
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
            plans[w["well_id"]] = p
            # independent re-computation of every headline number from the returned plans
            pump_m = {"spm": p["pump"]["spm"], "kd": p["pump"]["kd"]}
            pm = twin_value(w, p["mantle"], {**pump_m, "risk_cost": 0.0, "feasible": True}, exact=True)
            pp = twin_value(w, PRACTICE, {"spm": PRACTICE_PUMP[0], "kd": PRACTICE_PUMP[1], "risk_cost": 0.0, "feasible": True}, exact=True)
            lift = (pm["cum_oil"] / pm["days"]) / (pp["cum_oil"] / pp["days"]) - 1.0
            econ = _economic_cutoff(w, p["mantle"], (pump_m["spm"], pump_m["kd"]))
            econ_p = _economic_cutoff(w, PRACTICE, PRACTICE_PUMP)
            rows.append({"seconds": p["seconds"], "dividend": p["coupling_dividend_inr"],
                         "joint_ge_seq": p["joint"]["value_inr"] / p["per_cycle"]["mantle_days"] >= p["sequential"]["inr_per_day"] - 1e-6,
                         "gain": p["inr_per_cycle"], "oil_lift": p["oil_lift"], "sor_p": p["sor"][0], "sor_m": p["sor"][1],
                         "lift_err": abs(lift - p["oil_lift"]), "sor_err": abs(pm["sor"] - p["sor"][1]) + abs(pp["sor"] - p["sor"][0]),
                         "cutoff_m": p["mantle"]["cutoff"], "cutoff_econ_m": econ, "cutoff_econ_p": econ_p,
                         "moved_cutoff": p["mantle"]["cutoff"] != PRACTICE["cutoff"], "moved_soak": p["mantle"]["soak"] != PRACTICE["soak"],
                         "m2_vs_twin": abs(p["m2_check"]["joint_vs_twin"]),
                         "in_range": all(RANGES[k][0] <= p["mantle"][k] <= RANGES[k][1] for k in RANGES)})
        R = {k: np.array([r[k] for r in rows], dtype=float) for k in rows[0]}
        met = {"n_wells": len(rows), "seconds_max": float(R["seconds"].max()), "seconds_mean": float(R["seconds"].mean()),
               "joint_ge_sequential_all": bool(R["joint_ge_seq"].all()), "ranges_valid_all": bool(R["in_range"].all()),
               "coupling_dividend_inr_mean": float(R["dividend"].mean()),
               "gain_vs_practice_inr_mean_twin_verified": float(R["gain"].mean()),
               "share_wells_twin_gain_positive": float((R["gain"] > 0).mean()),
               "oil_lift_mean_twin_verified": float(R["oil_lift"].mean()),
               "sor_practice_mean": float(R["sor_p"].mean()), "sor_mantle_mean": float(R["sor_m"].mean()),
               "reverify_oil_lift_max_abs_err": float(R["lift_err"].max()), "reverify_sor_max_abs_err": float(R["sor_err"].max()),
               "share_wells_cutoff_moved": float(R["moved_cutoff"].mean()), "share_wells_soak_moved": float(R["moved_soak"].mean()),
               "cutoff_mantle_mean": float(R["cutoff_m"].mean()), "cutoff_economic_rule_mean": float(R["cutoff_econ_m"].mean()),
               "cutoff_economic_rule_practice_mean": float(R["cutoff_econ_p"].mean()),
               "m2_cum_oil_vs_twin_abs_mean": float(R["m2_vs_twin"].mean())}
    d = common.model_dir(ID, root)
    (d / "plans.json").write_text(json.dumps(_round(plans), separators=(",", ":")))
    meta = {"version": "1.1.0" + ("-quick" if quick else ""), "source": "physics_synthetic", "trained_at": common.now_iso(),
            "data_hash": common.data_hash([str(sorted(plans))]), "budget_s": budget}
    (d / "meta.json").write_text(json.dumps(meta))
    ev = {"metrics": met, "primary": {"name": "gain_vs_practice_inr_per_cycle_twin_verified", "value": met["gain_vs_practice_inr_mean_twin_verified"],
                                     "target": 0.0, "target_text": "> 0 (no numeric target in spec)", "baseline_name": "practice (L13)", "baseline": 0.0,
                                     "direction": "higher"},
          "train_seconds": tm["seconds"], "source": "physics_synthetic", "version": meta["version"], "data_hash": meta["data_hash"], "quick": quick}
    card = f"""# O2 CSS planner
Optuna TPE over steam t, injection pressure, soak d and cut-off d with the O1 pump optimum nested (joint) versus steam-first-then-pump (sequential), scored as
**net value per calendar day of a repeating cycle** (injection + soak + production days in the denominator, so the cut-off and soak matter). **Source: physics_synthetic**.
No weights: `train` runs the planner on {met["n_wells"]} wells (budget {budget:.0f} s each), re-runs the chosen, sequential and practice plans on the exact twin
(`synth.wellmodel.cycle_run`, the basis of the API's `/state`), reports those twin numbers, and caches the plans (with plan curves) in `plans.json`.
- Metrics: {json.dumps(met)}
- Steam volume is searched within +-25 % of the practice volume (`STEAM_TRUST`): the twin's per-day optimum is flat down to the 500 t bound, and a 30 % cut per cycle is neither a defensible operating change nor inside the data M1/M2 were trained on.
- Reported per plan: oil lift (oil per calendar day vs practice), SOR (`economics.sor` on cumulative oil to the plan's cut-off = the twin's `sor` metric at that day), INR per cycle
  (margin gain over one practice cycle of calendar time), coupling dividend = joint - sequential on the same basis. Joint >= sequential >= practice by construction on the twin (fallbacks are flagged).
- M2 gives the P10-P90 band and is reported as a cross-check (`m2_check`); it is not the score. Practice baseline is the fixture (800 t, 9 MPa, 4 d, 120 d at 5.4 SPM).
- Limits: injection pressure is a modelling assumption (no pressure physics in the twin); no cross-cycle decline (the twin has none; M2 carries it in the band only); the plan is checked against the twin, not against field results;
  cut-off is on the twin's day axis; chemical/maintenance day-rates are outside the objective (the twin's cut-off rule ignores them too).
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
