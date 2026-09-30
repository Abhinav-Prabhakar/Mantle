"""Per-well extension of the twin by composition (no change to mantle_physics formulas).

The twin models one well. Field variety comes from scaling its outputs: a productivity multiplier on oil,
a viscosity multiplier, a steam-efficiency multiplier on the effective steam volume fed to the thermal
model, cycle-to-cycle decline, and a soak-length effect. Day-by-day curves reuse ``pump.core`` /
``reservoir.base_arr`` exactly as ``economics.cycle`` does, but keep the extra columns S2/S5 need.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from mantle_physics.constants import CYCLE_DAYS, INJ_END, PRICE, SOAK_END
from mantle_physics.economics import sor as sor_fn
from mantle_physics.pump import core
from mantle_physics.reservoir import base_arr, thermal
from mantle_physics.rods import kd_table

BASE_SOAK_DAYS = SOAK_END - INJ_END      # 4 days in the twin


def soak_factor(soak_days: float) -> float:
    """Mild concave heat-distribution benefit of soaking (optimum ~7 d); 1.0 at the twin's 4 d."""
    s = float(soak_days)
    return 1 + 0.015 * (min(s, 7) - BASE_SOAK_DAYS) - 0.012 * max(0.0, s - 7)


@dataclass
class CycleRun:
    """Production part of a cycle on the twin's day axis (index = twin cycle day 0..120)."""

    T: np.ndarray
    rh: np.ndarray
    mu: np.ndarray
    oil: np.ndarray
    water: np.ndarray
    liquid: np.ndarray
    wc: np.ndarray
    fill: np.ndarray
    spm_safe: np.ndarray
    margin: np.ndarray
    margin_raw: np.ndarray
    goodman: np.ndarray
    kw: np.ndarray
    pprl: np.ndarray
    mprl: np.ndarray


def cycle_run(steam: float, spm: float, kd: float, *, steam_eff: float = 1.0, oil_scale: float = 1.0,
              visc_factor: float = 1.0, soak_days: float = BASE_SOAK_DAYS) -> CycleRun:
    # integer steam: mantle_physics caches per-integer steam, so rounding keeps results order-independent
    eff_steam = float(np.clip(round(steam * steam_eff), 300, 1400))
    pb = base_arr(eff_steam)
    kt = kd_table(kd)
    n = CYCLE_DAYS + 1
    a = {k: np.zeros(n) for k in
         ("T", "rh", "mu", "oil", "water", "liquid", "wc", "fill", "spm_safe", "margin", "margin_raw",
          "goodman", "kw", "pprl", "mprl")}
    k_oil = oil_scale * soak_factor(soak_days)
    for d in range(n):
        b = pb[d]
        prod = d >= SOAK_END
        c = core(b if prod else pb[SOAK_END], spm, kt)
        a["T"][d] = b.T
        a["rh"][d] = thermal(eff_steam, d).rh
        a["mu"][d] = b.muPump * visc_factor
        # oil/water scale linearly with the productivity multiplier (pump limit ignored for the small
        # multipliers used: pump displacement caps fillage at 0.98 in core()).
        a["oil"][d] = c.oil * k_oil if prod else 0.0
        a["liquid"][d] = c.q * k_oil if prod else 0.0
        a["water"][d] = a["liquid"][d] * c.wc if prod else 0.0
        a["wc"][d] = c.wc if prod else 0.0
        a["fill"][d] = min(0.98, c.fill * k_oil**0.6) if prod else 0.0
        a["spm_safe"][d] = c.spmSafe
        a["margin"][d] = c.margin
        a["margin_raw"][d] = c.marginRaw
        a["goodman"][d] = c.goodman
        a["kw"][d] = c.motorKw if prod else 0.0
        a["pprl"][d] = c.pprl
        a["mprl"][d] = c.mprl
    return CycleRun(**a)


def cycle_totals(run: CycleRun, steam: float, cutoff_day: int) -> dict[str, float]:
    """Cum oil/water (bbl, trapezoid) to ``cutoff_day`` and the derived economics."""
    d0, d1 = SOAK_END, int(cutoff_day)
    oil = run.oil[d0: d1 + 1]
    wat = run.water[d0: d1 + 1]
    cum_oil = float(np.trapezoid(oil))
    cum_w = float(np.trapezoid(wat))
    net_prod = float(np.trapezoid(run.oil[d0: d1 + 1] * PRICE["oil"] - run.kw[d0: d1 + 1] * 24 * PRICE["kwh"]))
    net = net_prod - steam * PRICE["steamT"]
    return {"cum_oil": cum_oil, "cum_water": cum_w, "net_inr": net, "sor": sor_fn(steam, cum_oil)}


def best_cutoff(run: CycleRun, steam: float, lo: int = 60) -> int:
    """Marginal-value cutoff (same rule as ``days_to_cutoff``): day of best whole-cycle average margin."""
    net_ex = run.oil * PRICE["oil"] - run.kw * 24 * PRICE["kwh"]
    cost = PRICE["steamT"] * steam
    cum, best, dcut = 0.0, -np.inf, CYCLE_DAYS
    for d in range(SOAK_END + 1, CYCLE_DAYS + 1):
        cum += (net_ex[d - 1] + net_ex[d]) / 2
        avg = (cum - cost) / d
        if avg > best:
            best, dcut = avg, d
    return max(lo, dcut)
