"""Seed-variable samplers: spec variables come from the physics-synthetic tables (S1/S2/S4/S5)."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ..paths import synthetic_dir
from ..synth.common import SEED, rng_for

ALARMS = ["PUMP_OFF", "HIGH_AMPS", "LOW_LOAD", "VFD_TRIP", "HIGH_THP", "LOW_FLOWLINE_T", "LOAD_CELL_FAULT",
          "ROD_FLOAT_RISK", "GOODMAN_HIGH", "GAS_LOCK"]
TOPICS = ["rod float", "fluid pound", "SOR", "cut-off timing", "soak length", "VFD profile",
          "asphaltene deposition", "pump unseating"]
JOB_TYPES = ["rod job", "pump change", "tubing leak repair", "stuffing box repack", "VFD fault",
             "belt/sheave change", "gearbox oil change", "counterbalance adjustment"]
DECISIONS = ["cycle steam volume", "soak length", "production cut-off day", "pump speed (SPM) setting",
             "VFD speed profile", "when to pull rods", "hold-down selection", "when to re-steam"]
CONDITIONS = ["cycle 1-3, viscosity above 1000 cP", "late cycle with falling fillage", "low reservoir pressure",
              "summer ambient above 45 C", "steam generator derated", "rod float alarms in the last week",
              "asphaltene deposition in tubing", "high water cut after cycle 6"]
COMPONENTS = ["rod body", "rod pin/coupling", "sinker bar", "polished rod", "pony rod"]
UNITS_OTSG = ["OTSG-1", "OTSG-2", "OTSG-3"]


@dataclass
class Context:
    wells: pd.DataFrame
    cycles: pd.DataFrame
    failures: pd.DataFrame
    unseats: pd.DataFrame
    daily: pd.DataFrame

    @classmethod
    def load(cls, synthetic: Path | None = None) -> Context:
        d = Path(synthetic) if synthetic else synthetic_dir()
        names = ("wells", "cycles", "failures", "unseats", "cycle_daily")
        if all((d / f"{n}.parquet").exists() for n in names):
            t = {n: pd.read_parquet(d / f"{n}.parquet") for n in names}
            return cls(t["wells"], t["cycles"], t["failures"], t["unseats"], t["cycle_daily"])
        return cls.generate("small")

    @classmethod
    def generate(cls, scale: str = "small") -> Context:
        from ..synth import s1_roster, s2_cycles, s5_failures

        w = s1_roster.generate(scale)
        c, d = s2_cycles.generate(w, scale)
        f, u, _ = s5_failures.generate(w, c, d)
        return cls(w, c, f, u, d)


def _fmt(v: Any) -> Any:
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, (date, datetime, pd.Timestamp)):
        return str(v)[:10]
    return v


def _well(ctx: Context, rng: np.random.Generator) -> dict:
    return ctx.wells.iloc[int(rng.integers(0, len(ctx.wells)))].to_dict()


def _rand_date(rng: np.random.Generator) -> str:
    return str(date(2024, 1, 1) + timedelta(days=int(rng.integers(0, 900))))


def _facts(w: dict) -> str:
    keys = ["api", "asphaltene_wt_pct", "t_res_c", "p_res_mpa", "pump_bore_in", "pump_depth_m", "unit_class",
            "stroke_m", "vfd_kw", "net_pay_m", "porosity", "perm_md"]
    return json.dumps({k: _fmt(w[k]) for k in keys})


def s_l1(ctx, rng, i):
    w = _well(ctx, rng)
    return {"well_id": w["well_id"], "spud_date": _fmt(w["spud_date"]), "pump_depth": _fmt(w["pump_depth_m"]),
            "perf_top": _fmt(w["perf_top_m"]), "perf_bot": _fmt(w["perf_bot_m"]), "physics_facts": _facts(w)}


def s_l2(ctx, rng, i):
    c = ctx.cycles.iloc[int(rng.integers(0, len(ctx.cycles)))].to_dict()
    prev = ctx.cycles[(ctx.cycles.well_id == c["well_id"]) & (ctx.cycles.cycle_no == c["cycle_no"] - 1)]
    ps = ("none (first cycle)" if prev.empty else json.dumps(
        {k: _fmt(prev.iloc[0][k]) for k in ("steam_t", "soak_days", "cum_oil_bbl", "sor", "net_inr")}))
    act = json.dumps({k: _fmt(c[k]) for k in ("steam_t", "soak_days", "cutoff_day", "cum_oil_bbl", "sor")})
    return {"well_id": c["well_id"], "n": int(c["cycle_no"]), "prev_cycle_summary": ps, "actuals": act}


def s_l3(ctx, rng, i):
    if len(ctx.failures):
        f = ctx.failures.iloc[int(rng.integers(0, len(ctx.failures)))].to_dict()
        depth = _fmt(f["depth_m"]) if f["depth_m"] == f["depth_m"] else 0
        gd = _fmt(f["goodman"]) if f["goodman"] == f["goodman"] else 0.8
        return {"well_id": f["well_id"], "date": _fmt(f["date"]), "component": str(rng.choice(COMPONENTS)),
                "depth": depth, "mode": f["mode"], "float": round(float(rng.uniform(-0.1, 0.5)), 2),
                "goodman": gd, "impacts": int(rng.integers(0, 6000)),
                "corr": round(float(ctx.wells.set_index("well_id").loc[f["well_id"], "corrosion_index"]), 2)}
    w = _well(ctx, rng)
    return {"well_id": w["well_id"], "date": _rand_date(rng), "component": str(rng.choice(COMPONENTS)),
            "depth": round(float(rng.uniform(100, 1000))), "mode": "fatigue", "float": 0.2,
            "goodman": round(float(rng.uniform(0.7, 1.1)), 2), "impacts": 1000, "corr": 0.4}


def s_l4(ctx, rng, i):
    if len(ctx.unseats):
        u = ctx.unseats.iloc[int(rng.integers(0, len(ctx.unseats)))].to_dict()
        return {"well_id": u["well_id"], "date": _fmt(u["date"]), "day": int(u["cycle_day"]),
                "mu": round(float(u["viscosity_cp"]))}
    w = _well(ctx, rng)
    return {"well_id": w["well_id"], "date": _rand_date(rng), "day": int(rng.integers(19, 100)), "mu": 300}


def s_l5(ctx, rng, i):
    w = _well(ctx, rng)
    return {"well_id": w["well_id"], "type": str(rng.choice(JOB_TYPES))}


def s_l6(ctx, rng, i):
    w = _well(ctx, rng)
    ev = rng.choice(["pump-off 02:10-03:05", "VFD trip 14:20", "THP rise to 0.9 MPa", "load cell reading flat 09:00",
                     "none"], size=2, replace=False)
    return {"k": 10, "well_id": w["well_id"], "date": _rand_date(rng), "events": "; ".join(ev)}


def s_l7(ctx, rng, i):
    w = _well(ctx, rng)
    ts = datetime(2026, 1, 1) + timedelta(minutes=int(rng.integers(0, 60 * 24 * 260)))
    snap = {"load_kn": round(float(rng.uniform(20, 105)), 1), "amps": round(float(rng.uniform(8, 32)), 1),
            "thp_mpa": round(float(rng.uniform(0.4, 1.2)), 2), "spm": round(float(rng.uniform(3, 7.5)), 1)}
    return {"alarm_code": str(rng.choice(ALARMS)), "well_id": w["well_id"], "ts": ts.strftime("%Y-%m-%d %H:%M IST"),
            "snapshot": json.dumps(snap)}


def s_l8(ctx, rng, i):
    from mantle_physics import DYNO_CLASSES, card_features, synthesize_cards

    lab = int(rng.integers(0, len(DYNO_CLASSES)))
    b = synthesize_cards([lab], rng)
    feats = card_features(b.surface_pos[0], b.surface_load[0], float(b.params["fluid_load"][0]))
    return {"card_features": json.dumps({k: round(float(v), 3) for k, v in feats.items()}),
            "label": DYNO_CLASSES[lab]}


def s_l9(ctx, rng, i):
    w = _well(ctx, rng)
    return {"well_id": w["well_id"], "date": _rand_date(rng), "A": round(float(w["walther_A"]), 3),
            "B": round(float(w["walther_B"]), 3)}


def s_l10(ctx, rng, i):
    c = ctx.cycles.iloc[int(rng.integers(0, len(ctx.cycles)))].to_dict()
    d = pd.Timestamp(c["start_date"]) + pd.Timedelta(days=int(rng.integers(0, 14)))
    plan = {"steam_t": _fmt(c["steam_t"]), "rate_t_per_d": _fmt(c["inj_rate_t_per_d"]),
            "pressure_mpa": _fmt(c["inj_pressure_mpa"]), "quality": _fmt(c["steam_quality"])}
    return {"unit": str(rng.choice(UNITS_OTSG)), "date": str(d)[:10], "plan": json.dumps(plan)}


def s_l11(ctx, rng, i):
    y = 2018 + int(i) % 9
    return {"period": f"FY {y}-{str(y + 1)[2:]} Q{int(rng.integers(1, 5))}"}


def s_l12(ctx, rng, i):
    w = _well(ctx, rng)
    cyc = ctx.cycles[ctx.cycles.well_id == w["well_id"]]
    facts = {"well": w["well_id"], "api": _fmt(w["api"]), "asphaltene_wt_pct": _fmt(w["asphaltene_wt_pct"])}
    if len(cyc):
        c = cyc.iloc[-1]
        facts |= {"latest_cycle": int(c["cycle_no"]), "steam_t": _fmt(c["steam_t"]), "sor": _fmt(c["sor"]),
                  "cum_oil_bbl": _fmt(c["cum_oil_bbl"]), "soak_days": _fmt(c["soak_days"])}
    return {"topic": str(rng.choice(TOPICS)), "well_id": w["well_id"], "facts": json.dumps(facts)}


def s_l13(ctx, rng, i):
    return {"decision": str(rng.choice(DECISIONS)), "conditions": str(rng.choice(CONDITIONS))}


SAMPLERS: dict[str, Callable[[Context, np.random.Generator, int], dict[str, Any]]] = {
    "L1": s_l1, "L2": s_l2, "L3": s_l3, "L4": s_l4, "L5": s_l5, "L6": s_l6, "L7": s_l7, "L8": s_l8, "L9": s_l9,
    "L10": s_l10, "L11": s_l11, "L12": s_l12, "L13": s_l13,
}


def sample_variables(spec_id: str, ctx: Context, index: int, seed: int = SEED) -> dict[str, Any]:
    """Deterministic variables for item ``index`` of a spec (independent of run order / resume)."""
    rng = rng_for(seed, "LLM-" + spec_id, index)
    return SAMPLERS[spec_id](ctx, rng, index)
