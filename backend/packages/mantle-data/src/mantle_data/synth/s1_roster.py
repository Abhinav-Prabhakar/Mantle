"""S1: field roster BGW-01..BGW-NN drawn from Baghewala ranges; BGW-17 is the showcase well."""

from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
import pandas as pd

from mantle_physics.constants import PUMP_DEPTH, S_M
from mantle_physics.viscosity import WAL_A, WAL_B, viscosity_cp

from .common import SEED, SHOWCASE_ID, SOURCE, Scale, get_scale, rng_for

UNITS = ["C-160D-173-64", "C-228D-213-86", "C-320D-256-100", "C-456D-256-120"]
TAPERS = ["1in/7/8in/3/4in + sinker", "7/8in/3/4in + sinker", "1in/7/8in/3/4in"]


def _walther_A(visc_factor: float) -> float:
    """Shift the Walther intercept so the 50 C viscosity is scaled by ``visc_factor``."""
    nu = viscosity_cp(50.0) / 0.96
    lo = math.log10(math.log10(nu + 0.7))
    hi = math.log10(math.log10(nu * visc_factor + 0.7))
    return WAL_A + (hi - lo)


def showcase_row() -> dict:
    return {
        "well_id": SHOWCASE_ID, "name": "Baghewala BGW-17", "spud_date": date(2024, 2, 14),
        "depth_m": 1165.0, "perf_top_m": 1100.0, "perf_bot_m": 1140.0, "net_pay_m": 40.0,
        "porosity": 0.27, "perm_md": 1800.0, "oil_saturation": 0.68, "api": 18.0,
        "asphaltene_wt_pct": 9.2, "t_res_c": 47.0, "p_res_mpa": 3.1, "casing_od_in": 7.0,
        "tubing_od_in": 2.875, "rod_taper": TAPERS[0], "pump_bore_in": 1.25, "pump_depth_m": float(PUMP_DEPTH),
        "unit_class": UNITS[1], "stroke_m": float(S_M), "vfd_kw": 22.0,
        "pi_factor": 1.0, "visc_factor": 1.0, "decline_rate": 0.9, "steam_eff": 1.0,
        "walther_A": WAL_A, "walther_B": WAL_B, "corrosion_index": 0.35,
        "is_showcase": True, "source": SOURCE,
    }


def generate(scale: str | Scale = "default", seed: int = SEED) -> pd.DataFrame:
    sc = get_scale(scale)
    rng = rng_for(seed, "S1")
    rows = []
    for i in range(1, sc.n_wells + 1):
        wid = f"BGW-{i:02d}"
        # draw for every well (so the stream is independent of the showcase override)
        perm = float(np.exp(rng.normal(math.log(1800), 0.45)))
        pay = float(rng.uniform(22, 55))
        perf_top = float(rng.uniform(1085, 1125))
        visc_f = float(np.exp(rng.normal(0, 0.15)))
        pi = float((perm / 1800) ** 0.25 * (pay / 40) ** 0.6 * np.exp(rng.normal(0, 0.12)))
        row = {
            "well_id": wid, "name": f"Baghewala {wid}",
            "spud_date": date(2011, 1, 1) + timedelta(days=int(rng.integers(0, 3800))),
            "depth_m": perf_top + pay + float(rng.uniform(15, 35)),
            "perf_top_m": perf_top, "perf_bot_m": min(perf_top + pay, 1160.0 + 20),
            "net_pay_m": pay,
            "porosity": float(rng.uniform(0.24, 0.30)), "perm_md": perm,
            "oil_saturation": float(rng.uniform(0.60, 0.74)), "api": float(rng.uniform(17.0, 19.5)),
            "asphaltene_wt_pct": float(rng.uniform(7.0, 12.0)), "t_res_c": float(rng.uniform(46, 48)),
            "p_res_mpa": float(rng.uniform(2.6, 3.4)), "casing_od_in": 7.0,
            "tubing_od_in": float(rng.choice([2.375, 2.875])),
            "rod_taper": str(rng.choice(TAPERS)), "pump_bore_in": float(rng.choice([1.0, 1.25, 1.5, 1.75])),
            "pump_depth_m": float(rng.uniform(1040, 1090)), "unit_class": str(rng.choice(UNITS)),
            "stroke_m": float(S_M), "vfd_kw": float(rng.choice([18.5, 22.0, 30.0, 37.0])),
            "pi_factor": pi, "visc_factor": visc_f, "decline_rate": float(rng.uniform(0.85, 0.94)),
            "steam_eff": float(rng.uniform(0.88, 1.10)), "walther_A": _walther_A(visc_f), "walther_B": WAL_B,
            "corrosion_index": float(rng.uniform(0.1, 0.8)), "is_showcase": False, "source": SOURCE,
        }
        row["perf_bot_m"] = min(row["perf_bot_m"], row["depth_m"] - 5)
        if wid == SHOWCASE_ID:
            row = showcase_row()
        rows.append(row)
    df = pd.DataFrame(rows)
    df["spud_date"] = pd.to_datetime(df["spud_date"]).dt.date
    return df
