"""Whole-cycle curves, economics (INR) and the coupling dividend (from ``sim.js``)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from ._util import clamp
from .constants import (
    BBL_PER_T_CWE,
    CYCLE_DAYS,
    GRID_CO2_KG_KWH,
    INJ_END,
    MARGIN_REQ,
    PRICE,
    SOAK_END,
    STEAM_CO2_T_PER_T,
)
from .pump import core
from .reservoir import base_arr
from .rods import KdTable, kd_table


@dataclass
class CycleCurves:
    wat: list[float] = field(default_factory=list)
    T: list[float] = field(default_factory=list)
    mu: list[float] = field(default_factory=list)
    oil: list[float] = field(default_factory=list)
    wc: list[float] = field(default_factory=list)
    spm_safe: list[float] = field(default_factory=list)
    margin: list[float] = field(default_factory=list)
    cum: list[float] = field(default_factory=list)
    cum_w: list[float] = field(default_factory=list)
    net_ex: list[float] = field(default_factory=list)
    kw: list[float] = field(default_factory=list)


def cycle(steam: float, spm: float, kd: float) -> CycleCurves:
    """Arrays over day 0..120 for the whole steam cycle."""
    kt = kd_table(kd)
    pb = base_arr(steam)
    o = CycleCurves()
    cum = cum_w = 0.0
    for d in range(CYCLE_DAYS + 1):
        b = pb[d]
        prod = d >= SOAK_END
        c = core(b if prod else pb[SOAK_END], spm, kt)   # before production show the day-18 state
        oil = c.oil if prod else 0.0
        liq = c.q if prod else 0.0
        kw = c.motorKw if prod else 0.0
        if prod and d > SOAK_END:
            cum += (o.oil[d - 1] + oil) / 2
            cum_w += (o.wat[d - 1] + liq * c.wc) / 2
        o.T.append(b.T)
        o.mu.append(b.muPump)
        o.oil.append(oil)
        o.wc.append(c.wc if prod else 0.0)
        o.spm_safe.append(c.spmSafe)
        o.margin.append(c.margin)
        o.cum.append(cum)
        o.cum_w.append(cum_w)
        o.kw.append(kw)
        o.wat.append(liq * c.wc)
        o.net_ex.append(oil * PRICE["oil"] - kw * 24 * PRICE["kwh"])
    return o


def days_to_cutoff(cyc: CycleCurves, steam: float, day: float) -> float:
    """Marginal-value cutoff: leave when the daily margin falls below the best whole-cycle average."""
    steam_cost = PRICE["steamT"] * steam
    cum = 0.0
    best = -math.inf
    dcut = CYCLE_DAYS
    for d in range(SOAK_END + 1, CYCLE_DAYS + 1):
        cum += (cyc.net_ex[d - 1] + cyc.net_ex[d]) / 2
        avg = (cum - steam_cost) / d
        if avg > best:
            best = avg
            dcut = d
    return max(0.0, dcut - day)


def sor(steam: float, cum_oil: float) -> float:
    """Steam-oil ratio (bbl CWE steam per bbl oil), 0 until 5 bbl have been produced."""
    return clamp(steam * BBL_PER_T_CWE / cum_oil, 0, 99) if cum_oil > 5 else 0.0


def co2_per_bbl(steam: float, cum_oil: float, kwh_bbl: float) -> float:
    return min(400.0, steam * STEAM_CO2_T_PER_T * 1000 / max(cum_oil, 50) + kwh_bbl * GRID_CO2_KG_KWH)


def net_per_day(phase: str, steam: float, oil: float, kwh: float) -> float:
    steam_cost = PRICE["steamT"] * steam
    if phase == "PRODUCTION":
        return oil * PRICE["oil"] - steam_cost / (CYCLE_DAYS - SOAK_END) - kwh * PRICE["kwh"]
    if phase == "INJECTION":
        return -(steam / INJ_END) * PRICE["steamT"]
    return 0.0


# ---------------------------------------------------------------- coupling dividend

STEAM_GRID = [500, 600, 700, 800, 900, 1000, 1100]


def _spm_grid() -> list[float]:
    a = []
    s = 2.0
    while s <= 9.0001:
        a.append(float(f"{s:.2f}"))
        s += 0.5
    return a


SPM_GRID = _spm_grid()


@dataclass(frozen=True)
class Plan:
    steam: float
    spm: float
    val: float
    oil: float
    minM: float
    ok: bool


def eval_plan(steam: float, spm: float, kt: KdTable, reservoir_only: bool = False) -> Plan:
    pb = base_arr(steam)
    val = -steam * PRICE["steamT"]
    oil = 0.0
    min_m = 1.0
    for d in range(SOAK_END, CYCLE_DAYS + 1):
        if reservoir_only:      # lift assumed unlimited: pure reservoir response to steam
            o = pb[d].qIn * (1 - pb[d].wc)
            val += o * PRICE["oil"]
            oil += o
            continue
        c = core(pb[d], spm, kt)
        val += c.oil * PRICE["oil"] - c.motorKw * 24 * PRICE["kwh"]
        oil += c.oil
        min_m = min(min_m, c.marginRaw)
    return Plan(steam, spm, val, oil, min_m, min_m >= MARGIN_REQ)


@dataclass(frozen=True)
class Coupling:
    inrPerCycle: float
    oilPct: float
    jointSteam: float
    jointSpm: float
    seqSteam: float
    seqSpm: float


_COUPLING_CACHE: dict[int, Coupling] = {}


def _better(a: Plan | None, b: Plan) -> Plan:
    return b if (a is None or b.val > a.val) else a


def coupling_dividend(kd: float) -> Coupling:
    """Joint steam+pump optimum vs sequential (steam first at a nominal 6 SPM, then pump)."""
    key = math.floor(kd * 1000 + 0.5)
    hit = _COUPLING_CACHE.get(key)
    if hit is not None:
        return hit
    kt = kd_table(kd)
    seq_steam: Plan | None = None
    for st in STEAM_GRID:
        seq_steam = _better(seq_steam, eval_plan(st, 6, kt))
    assert seq_steam is not None
    seq: Plan | None = None
    joint: Plan | None = None
    fallback: Plan | None = None
    for spm in SPM_GRID:
        p = eval_plan(seq_steam.steam, spm, kt)
        if p.ok:
            seq = _better(seq, p)
        if fallback is None or p.minM > fallback.minM:
            fallback = p
    seq = seq or fallback
    j_fallback: Plan | None = None
    for st in STEAM_GRID:
        for spm in SPM_GRID:
            p = eval_plan(st, spm, kt)
            if p.ok:
                joint = _better(joint, p)
            if j_fallback is None or p.minM > j_fallback.minM:
                j_fallback = p
    joint = joint or j_fallback
    assert seq is not None and joint is not None
    res = Coupling(
        max(0.0, joint.val - seq.val),
        max(0.0, (joint.oil - seq.oil) / max(seq.oil, 1)),
        joint.steam, joint.spm, seq.steam, seq.spm,
    )
    _COUPLING_CACHE[key] = res
    return res
