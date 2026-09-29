"""Per-point engineering core (loads, float margin, fillage, Goodman) and the dynamometer load model."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._util import TAU, clamp, smooth
from .constants import (
    ETA_S,
    FRIC_FRAC,
    LBF_N,
    OIL_SG,
    PLUNGER_IN,
    PUMP_DEPTH,
    S_IN,
    S_M,
    SPM_MAX,
    TORQUE_RATING_INLB,
    WATER_SG,
    G,
)
from .reservoir import ProdBase
from .rods import APK_BASE, KX, SECT, W_R, KdTable, interp, w_below

PD_K = 0.1166 * S_IN * PLUNGER_IN * PLUNGER_IN    # bbl/d per SPM


def softmin(a: float, b: float, p: float = 10) -> float:
    return math.pow(math.pow(max(a, 1e-6), -p) + math.pow(max(b, 1e-6), -p), -1 / p)


@dataclass(frozen=True)
class Core:
    c: float
    wc: float
    Gfl: float
    Wrf: float
    Fo: float
    omega: float
    vUp: float
    vDn: float
    dUp: float
    dDn: float
    Ffric: float
    marginRaw: float
    margin: float
    spmSafe: float
    PDg: float
    PDe: float
    q: float
    fill: float
    oil: float
    alpha: float
    pprl: float
    mprl: float
    torque: float
    goodman: float
    motorKw: float
    level: float
    pumpEff: float
    bottleneck: str


def core(b: ProdBase, spm: float, kt: KdTable) -> Core:
    wc = b.wc
    Gfl = (1 - wc) * OIL_SG + wc * WATER_SG
    bf = 1 - 0.128 * Gfl
    Wrf = W_R * bf
    Fo = 0.340 * Gfl * PLUNGER_IN * PLUNGER_IN * (PUMP_DEPTH / 0.3048) * LBF_N
    omega = TAU * spm / 60
    vUp, vDn = omega * kt.vUp, omega * kt.vDn
    dUp, dDn = b.c * vUp, b.c * vDn
    Ffric = FRIC_FRAC * Wrf
    margin_raw = 1 - (dDn + Ffric) / Wrf
    margin = clamp(margin_raw, -1, 1)
    k_safe = b.c * (TAU / 60) * kt.vDn
    spm_safe = clamp((0.85 * Wrf - Ffric) / k_safe, 0.5, SPM_MAX) if k_safe > 1e-9 else SPM_MAX
    eta_float = 1 - clamp(-margin_raw * 0.8, 0, 0.5)
    PDg = PD_K * spm
    PDe = max(1e-6, PDg * ETA_S * eta_float)
    q = softmin(b.qIn, PDe)
    fill = clamp(q / PDe, 0, 0.98)
    oil = q * (1 - wc)
    alpha = (S_IN * spm * spm / 70500) * (kt.aPk / APK_BASE)
    pprl = (Wrf + Fo + W_R * alpha + dUp) / 1000
    mprl = max(0.0, (Wrf - W_R * alpha - dDn) / 1000)
    torque = clamp(0.25 * S_IN * ((pprl - mprl) * 1000 / LBF_N) * 0.55 / TORQUE_RATING_INLB, 0, 1.5)
    # Goodman at the top of each rod section (modified Goodman, Grade D 793 MPa, service factor 0.85)
    goodman = 0.0
    for X in (0, 500, 800):
        sec = next(s for s in SECT if s.top == X)
        wb = w_below(X)
        cb = b.c if X == 0 else b.c500 if X == 500 else b.c800
        smax = (wb * bf + Fo + wb * alpha + cb * vUp) / sec.A
        smin = max(0.0, (wb * bf - wb * alpha - cb * vDn) / sec.A)
        goodman = max(goodman, smax / (0.85 * (793 / 4 + 0.5625 * smin)))
    goodman = clamp(goodman, 0, 1.5)
    work = Fo * S_M * fill + b.c * omega * kt.iDrag       # J per stroke (card area)
    kw_pr = work * spm / 60 / 1000
    motor_kw = kw_pr / (0.85 * 0.9) + 0.5
    r = b.qIn / PDe
    level = 350 + 550 * (1 - smooth((r - 0.3) / 1.4))     # depth to fluid level (m)
    return Core(
        b.c, wc, Gfl, Wrf, Fo, omega, vUp, vDn, dUp, dDn, Ffric, margin_raw, margin, spm_safe, PDg, PDe, q,
        fill, oil, alpha, pprl, mprl, torque, goodman, motor_kw, level,
        clamp(q / max(PDg, 1e-6), 0, 1), "PUMP" if b.qIn > PDe else "RESERVOIR",
    )


# ---------------------------------------------------------------- dynamometer load model


@dataclass(frozen=True)
class LoadModel:
    Wrf: float
    Wr: float
    Fo: float
    c: float
    xp: float
    w: float
    wDh: float
    amp: float
    strokeRatio: float


def load_model(c: Core, kt: KdTable | None = None) -> LoadModel:
    return LoadModel(
        Wrf=c.Wrf, Wr=W_R, Fo=c.Fo, c=c.c, xp=S_M * c.fill,
        w=S_M * (0.008 + 0.02 * (1 - c.fill)),
        wDh=S_M * (0.006 + 0.03 * (1 - c.fill)),
        amp=0.06 + 0.6 * max(0.0, 0.9 - c.fill),
        strokeRatio=ETA_S * (1 - clamp(-c.marginRaw * 0.8, 0, 0.5)) * 1.0 + (1 - ETA_S) * 0.5,
    )


def surface_point(m: LoadModel, kt: KdTable, theta: float, omega: float) -> tuple[float, float, bool]:
    """Instantaneous polished-rod position (m), load (kN) and upstroke flag at crank angle theta."""
    x = interp(KX, theta)
    V = interp(kt.V, theta)
    Ab = interp(kt.Ab, theta)
    v = omega * V
    ag = omega * omega * Ab / G
    up = V >= 0
    xp, w = m.xp, m.w
    F = m.Wrf + m.Wr * ag
    if up:
        d = x / S_M
        F += m.Fo * smooth(d / 0.06) + m.c * abs(v) + m.Fo * 0.04 * math.exp(-d / 0.07) * math.sin(TAU * d / 0.12)
    else:
        psi = 1 / (1 + math.exp(-(x - xp) / w))
        d = max(0.0, xp - x) / S_M
        F += (
            m.Fo * psi - m.c * abs(v)
            + m.Fo * m.amp * math.exp(-d / 0.08) * math.cos(TAU * d / 0.13) * (1 - psi)
        )
    eps = 0.02 * m.Wrf     # soft floor: rods cannot push
    F = 0.5 * (F + math.sqrt(F * F + eps * eps))
    return clamp(x, 0, S_M), F / 1000, up


def downhole_point(m: LoadModel, kt: KdTable, theta: float) -> tuple[float, float]:
    x = interp(KX, theta)
    V = interp(kt.V, theta)
    xd = x * m.strokeRatio
    if V >= 0:
        f = m.Fo * smooth(x / (0.035 * S_M))
    else:
        f = m.Fo / (1 + math.exp(-(x - m.xp) / m.wDh))
    return clamp(xd, 0, S_M), f / 1000
