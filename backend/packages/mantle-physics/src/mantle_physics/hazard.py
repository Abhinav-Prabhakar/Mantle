"""Physics-informed hazards: rod parting (Miner's-rule fatigue) and pump unseating.

Used to simulate failure histories (S5) and as physics features/baselines for the survival model (M4).

Rod fatigue
    Goodman ratio ``gr`` per rod (from the stress range along depth) -> damage per stroke
    ``(gr ** m) / N_ref`` (S-N line, ``N_ref`` strokes to failure at gr = 1). Damage is amplified by
    rod-float events (compressive buckling), impact loading (fluid pound) and corrosion. Miner's rule
    accumulates ``D``; failure occurs when a Weibull-distributed critical damage is reached, giving the
    hazard ``h = k * D**(k-1) * dD/dt`` (monotone in D and in the damage rate).

Pump unseating
    Upward force on the plunger/hold-down (viscous drag + fluid-pound impact + static) over hold-down
    capacity; hazard ~ ``h0 * ratio**p`` so it is negligible at low uplift and rises steeply near 1.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .rods import SECT

# ---- fatigue constants (calibrated so gr ~ 1 at ~8k strokes/day fails within months)
SN_EXPONENT = 8.0          # slope of the S-N line in Goodman-ratio space
N_REF = 1.0e6              # strokes to failure at Goodman ratio 1.0
WEIBULL_K = 3.5            # shape of the critical-damage distribution (scale 1)
FLOAT_AMP = 6.0            # extra damage multiplier per unit fraction of strokes with rod float
CORROSION_AMP = 1.5        # extra multiplier at corrosion index 1
IMPACT_STRESS_GAIN = 0.35  # extra Goodman ratio per m/s of plunger impact velocity
IMPACT_SPREAD = 0.25       # fraction of the string's peak stress felt by an impact pulse (attenuation)

N_RODS = 140
ROD_LENGTH_M = 7.62


def goodman_ratio(smax, smin, tensile_mpa: float = 793.0, service_factor: float = 0.85):
    """Modified-Goodman ratio (as in the twin): smax / (SF * (T/4 + 0.5625 * smin)); stresses in MPa."""
    smax = np.asarray(smax, dtype=float)
    smin = np.maximum(np.asarray(smin, dtype=float), 0.0)
    return smax / (service_factor * (tensile_mpa / 4 + 0.5625 * smin))


def rod_stress_by_depth(depths, fluid_load: float, alpha: float, drag_below, v_up: float, bf: float = 0.874):
    """Peak stress (MPa == N/mm2) at each depth, the same expression the twin's ``profile()`` uses."""
    depths = np.asarray(depths, dtype=float)
    out = np.zeros_like(depths)
    for i, z in enumerate(depths):
        sec = next((s for s in SECT if s.top <= z < s.bot), SECT[-1])
        wb = sum(s.w * max(0.0, s.bot - max(s.top, z)) for s in SECT)
        cb = drag_below[i] if hasattr(drag_below, "__len__") else drag_below
        out[i] = (wb * bf + fluid_load + wb * alpha + cb * v_up) / sec.A
    return out


def rod_damage_rate(
    goodman,
    strokes_per_day,
    float_frac=0.0,
    impacts_per_day=0.0,
    impact_vel=0.0,
    corrosion=0.0,
):
    """Miner damage accumulated per day (broadcasts over rods when ``goodman`` is an array).

    ``float_frac``: fraction of strokes with rod float; ``impacts_per_day`` / ``impact_vel`` (m/s):
    fluid-pound count and plunger impact velocity; ``corrosion``: 0..1 index.
    """
    gr = np.maximum(np.asarray(goodman, dtype=float), 0.0)
    base = strokes_per_day * gr**SN_EXPONENT / N_REF
    amp = (1 + FLOAT_AMP * np.clip(float_frac, 0, 1)) * (1 + CORROSION_AMP * np.clip(corrosion, 0, 1))
    gr_imp = gr * IMPACT_SPREAD * (1 + IMPACT_STRESS_GAIN * np.maximum(impact_vel, 0))
    impact = impacts_per_day * gr_imp**SN_EXPONENT / N_REF
    return base * amp + impact


def rod_hazard_rate(damage, damage_rate):
    """Failure hazard (per day) at accumulated Miner damage ``damage`` accruing ``damage_rate`` per day."""
    d = np.maximum(np.asarray(damage, dtype=float), 1e-12)
    return WEIBULL_K * d ** (WEIBULL_K - 1) * np.asarray(damage_rate, dtype=float)


def rod_failure_probability(damage0, damage_rate, days: float):
    """P(failure within ``days``) for a rod at damage ``damage0`` accruing linearly at ``damage_rate``."""
    d0 = np.asarray(damage0, dtype=float)
    d1 = d0 + np.asarray(damage_rate, dtype=float) * days
    return 1 - np.exp(-(d1**WEIBULL_K - d0**WEIBULL_K))


# ---------------------------------------------------------------- pump unseating

VISC_DRAG_N_PER_PAS_MS = 8333.0   # viscous plunger drag ~ 2.5 kN at 1000 cP and 0.3 m/s
BASE_UPLIFT_KN = 9.0              # hydrostatic + friction share of the hold-down load
POUND_UPLIFT_KN = 8.0             # extra uplift at full fluid pound
UNSEAT_H0 = 0.02                  # per-day hazard when uplift == hold-down capacity
UNSEAT_POWER = 6.0


def pump_uplift_kn(mu_cp, v_up, fillage, impact_vel=0.0):
    """Upward force (kN) trying to lift the pump off its seat: viscous drag + pound impacts + static."""
    mu_pas = np.asarray(mu_cp, dtype=float) / 1000.0
    visc = VISC_DRAG_N_PER_PAS_MS * mu_pas * np.asarray(v_up, dtype=float) / 1000.0
    pound = np.clip((0.85 - np.asarray(fillage, dtype=float)) / 0.35, 0, 1)
    return BASE_UPLIFT_KN + visc + POUND_UPLIFT_KN * pound * (1 + 0.5 * np.maximum(impact_vel, 0))


def pump_unseat_hazard(uplift_kn, hold_down_kn: float = 18.0):
    """Per-day unseating hazard; monotone in uplift, tiny when uplift << hold-down."""
    ratio = np.maximum(np.asarray(uplift_kn, dtype=float), 0.0) / hold_down_kn
    return UNSEAT_H0 * ratio**UNSEAT_POWER


# ---------------------------------------------------------------- failure-history simulation


@dataclass
class RodFailure:
    day: int
    rod: int            # 0-based rod index from surface
    depth_m: float
    goodman: float
    mode: str           # "fatigue" | "float-buckling"


def simulate_rod_failures(
    rng: np.random.Generator,
    goodman_by_rod,
    strokes_per_day,
    days: int,
    float_frac=0.0,
    impacts_per_day=0.0,
    impact_vel=0.0,
    corrosion=0.0,
    n_rods: int = N_RODS,
) -> list[RodFailure]:
    """Simulate rod parts over ``days`` with constant conditions (each failure resets the failed rod).

    ``goodman_by_rod`` is an ``(n_rods,)`` array (top to bottom) or a scalar. The first failure per rod
    occurs when its Miner damage reaches a Weibull(k) critical value drawn via inverse transform.
    """
    gr = np.broadcast_to(np.asarray(goodman_by_rod, dtype=float), (n_rods,))
    rate = rod_damage_rate(gr, strokes_per_day, float_frac, impacts_per_day, impact_vel, corrosion)
    out: list[RodFailure] = []
    for i in range(n_rods):
        t = 0.0
        while rate[i] > 0:
            d_crit = (rng.exponential(1.0)) ** (1 / WEIBULL_K)
            t += d_crit / rate[i]
            if t > days:
                break
            mode = "float-buckling" if rng.random() < min(0.9, float_frac * FLOAT_AMP / (1 + FLOAT_AMP * float_frac)) else "fatigue"
            out.append(RodFailure(int(t), i, (i + 0.5) * ROD_LENGTH_M, float(gr[i]), mode))
    out.sort(key=lambda f: f.day)
    return out

