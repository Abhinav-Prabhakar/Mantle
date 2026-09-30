"""Thermal history, Boberg-Lantz style inflow and wellbore temperature / drag (from ``sim.js``)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._util import clamp
from .constants import (
    CYCLE_DAYS,
    INJ_END,
    KVIS,
    MU_CAP_CP,
    PUMP_DEPTH,
    PUMP_INTAKE,
    SOAK_END,
    T_RES,
    TAU,
    Z_SAND,
)
from .rods import SECT
from .viscosity import MU_COLD, viscosity_cp


@dataclass(frozen=True)
class Thermal:
    phase: str
    T: float
    exc: float
    exc0: float
    rh: float
    rh0: float
    battery: float


def thermal(steam: float, day: float) -> Thermal:
    """Steam scale s = steam/800 t. exc0 = sandface excess over reservoir at end of soak."""
    s = max(0.2, steam / 800)
    g = (1 - math.exp(-4.5 * s)) / (1 - math.exp(-4.5))
    exc0 = 143 * (0.3 + 0.7 * g)
    rh0 = 11 * (0.6 + 0.4 * g)
    tau = 40 * math.pow(s, 0.2)
    if day < INJ_END:
        phase = "INJECTION"
        exc = 1.04 * exc0 * (1 - math.exp(-day / 5)) / (1 - math.exp(-INJ_END / 5))
        rh = rh0 * math.sqrt(day / INJ_END)
    elif day < SOAK_END:
        phase = "SOAK"
        exc = exc0 * (1.04 - 0.04 * (day - INJ_END) / (SOAK_END - INJ_END))
        rh = rh0
    else:
        phase = "PRODUCTION"
        t = day - SOAK_END
        exc = exc0 * math.exp(-t / tau)
        rh = rh0 * (0.75 + 0.25 * math.exp(-t / 38))
    return Thermal(phase, T_RES + exc, exc, exc0, rh, rh0, clamp(exc / exc0, 0, 1))


RW, RE = 0.11, 40.0


def steam_mult(s: float) -> float:
    return (1 - math.exp(-4 * s)) / (1 - math.exp(-4))


def prod_ratio(T: float, rh: float) -> float:
    """Hot zone of radius rh in series with the cold outer zone."""
    mu_h = viscosity_cp(T_RES + 0.65 * (T - T_RES))
    R = max(rh, RW * 1.5)
    return (MU_COLD * math.log(RE / RW)) / (mu_h * math.log(R / RW) + MU_COLD * math.log(RE / R))


DEPLETION_TAU = 220.0


def _q0() -> float:
    th = thermal(800, 20)
    return 82 / (prod_ratio(th.T, th.rh) * math.exp(-2 / DEPLETION_TAU))


Q0 = _q0()


def water_cut(t: float) -> float:
    return 0.15 + 0.20 * (1 - math.exp(-max(0.0, t) / 70))


def t_geo(z: float) -> float:
    return 28 + 19 * z / 1120


def t_fluid(z: float, exc: float, Lr: float) -> float:
    """Flowing fluid temperature at depth z."""
    if z >= Z_SAND:
        return t_geo(z) + exc * math.exp(-(z - Z_SAND) / 60)
    return t_geo(z) + exc * math.exp(-(Z_SAND - z) / Lr)


def drag_coeff(exc: float, Lr: float) -> dict[str, float]:
    """Couette-annulus drag coefficient c (N*s/m): F_drag = c*|v_rod|; c500/c800 = share below depths."""
    dz = 12.0
    c = c500 = c800 = 0.0
    z = dz / 2
    while z < PUMP_DEPTH:
        mu = min(viscosity_cp(t_fluid(z, exc, Lr)), MU_CAP_CP) * KVIS / 1000
        sec = SECT[0] if z < 500 else SECT[1] if z < 800 else SECT[2]
        d = TAU * mu * dz / sec.lnr
        c += d
        if z >= 500:
            c500 += d
        if z >= 800:
            c800 += d
        z += dz
    return {"c": c, "c500": c500, "c800": c800}


@dataclass(frozen=True)
class ProdBase:
    """Per-day production base state (independent of spm/kd)."""

    day: float
    th: Thermal
    T: float
    rh: float
    qIn: float
    wc: float
    Lr: float
    muPump: float
    Tpump: float
    c: float
    c500: float
    c800: float


def prod_base(steam: float, day: float) -> ProdBase:
    th = thermal(steam, day)
    dp = max(day, SOAK_END)
    tp = thermal(steam, dp)
    t = dp - SOAK_END
    q_in = Q0 * steam_mult(max(0.2, steam / 800)) * prod_ratio(tp.T, tp.rh) * math.exp(-t / DEPLETION_TAU)
    wc = water_cut(t)
    parked = th.phase != "PRODUCTION"
    Lr = 4000.0 if parked else 250 + 5 * q_in
    drag = drag_coeff(th.exc, Lr)
    Tpump = t_fluid(PUMP_INTAKE, th.exc, Lr)
    return ProdBase(day, th, th.T, th.rh, q_in, wc, Lr, viscosity_cp(Tpump), Tpump, **drag)


_BASE_CACHE: dict[int, list[ProdBase]] = {}


def base_arr(steam: float) -> list[ProdBase]:
    """Integer days 0..120 for a given steam volume (cached like the JS, 40-entry reset)."""
    key = math.floor(steam + 0.5)
    a = _BASE_CACHE.get(key)
    if a is None:
        a = [prod_base(steam, d) for d in range(CYCLE_DAYS + 1)]
        if len(_BASE_CACHE) > 40:
            _BASE_CACHE.clear()
        _BASE_CACHE[key] = a
    return a


def deposition(exc: float, Lr: float) -> tuple[float | None, float | None]:
    """Asphaltene deposition band: fluid cooler than the 62 C onset, above the pump."""
    bot = None
    z = PUMP_DEPTH
    while z >= 0:
        if t_fluid(z, exc, Lr) < 62:
            bot = z
            break
        z -= 10
    if bot is None:
        return None, None
    return max(20.0, bot - 220), bot
