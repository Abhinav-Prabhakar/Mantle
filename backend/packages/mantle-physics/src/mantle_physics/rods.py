"""Rod string and crank kinematics tables (from ``sim.js``)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ._util import TAU, clamp, js_mod
from .constants import PUMP_DEPTH
from .rig import rod_position


@dataclass(frozen=True)
class RodSection:
    top: float
    bot: float
    A: float      # mm2
    w: float      # N/m in air, incl. couplings and sinker/heavy rods
    lnr: float    # ln(Dt/Dr) for the Couette annulus


# 1-1/8", 1", 7/8"
SECT = [
    RodSection(0, 500, 641, 67, math.log(62 / 28.575)),
    RodSection(500, 800, 506.7, 53, math.log(62 / 25.4)),
    RodSection(800, PUMP_DEPTH, 387.9, 40.6, math.log(62 / 22.2)),
]
W_R = sum(s.w * (s.bot - s.top) for s in SECT)   # N in air


def w_below(X: float) -> float:
    return sum(s.w * max(0.0, s.bot - max(s.top, X)) for s in SECT)


# ---------------------------------------------------------------- crank kinematics tables

NK = 720
HK = TAU / NK
KX = [rod_position(i * HK) for i in range(NK)]
KXP = [(KX[(i + 1) % NK] - KX[(i - 1 + NK) % NK]) / (2 * HK) for i in range(NK)]
XP_MAX = max(abs(b) for b in KXP)


def _refine(theta0: float, sign: int) -> float:
    """Golden-section on rod_position around a table extremum."""
    a, b = theta0 - HK, theta0 + HK
    gr = 0.6180339887
    for _ in range(40):
        c = b - gr * (b - a)
        d = a + gr * (b - a)
        if sign * rod_position(c) > sign * rod_position(d):
            b = d
        else:
            a = c
    return js_mod(js_mod((a + b) / 2, TAU) + TAU, TAU)


def _extreme(sign: int) -> float:
    k = 0
    for i in range(NK):
        if (KX[i] > KX[k]) if sign > 0 else (KX[i] < KX[k]):
            k = i
    return _refine(k * HK, sign)


TH_TOP = _extreme(1)
TH_BOT = _extreme(-1)


def interp(arr: list[float], theta: float) -> float:
    """Periodic linear interpolation of a 720-point crank table."""
    u = js_mod(js_mod(theta, TAU) + TAU, TAU) / HK
    i = math.floor(u)
    f = u - i
    return arr[i % NK] * (1 - f) + arr[(i + 1) % NK] * f


@dataclass(frozen=True)
class KdTable:
    """Per-kd shaped velocity V (m per rad of crank), acceleration Ab and peak values."""

    kd: float
    s: list[float]
    V: list[float]
    Ab: list[float]
    vUp: float
    vDn: float
    aPk: float
    iDrag: float


_KT_CACHE: dict[int, KdTable] = {}


def kd_table(kd: float) -> KdTable:
    """VFD stroke shaping: downstroke at 0.5/kd of nominal crank speed, upstroke at 0.5/(1-kd)."""
    key = math.floor(kd * 1000 + 0.5)
    t = _KT_CACHE.get(key)
    if t is not None:
        return t
    k = clamp(key / 1000, 0.35, 0.75)
    s_up, s_dn = 0.5 / (1 - k), 0.5 / k
    s = [0.0] * NK
    V = [0.0] * NK
    Ab = [0.0] * NK
    for i in range(NK):
        w = 0.5 * (1 + math.tanh(KXP[i] / (0.04 * XP_MAX)))
        s[i] = w * s_up + (1 - w) * s_dn
        V[i] = KXP[i] * s[i]
    v_up = v_dn = a_pk = i_drag = 0.0
    for i in range(NK):
        Ab[i] = s[i] * (V[(i + 1) % NK] - V[(i - 1 + NK) % NK]) / (2 * HK)
        v_up = max(v_up, V[i])
        v_dn = max(v_dn, -V[i])
        a_pk = max(a_pk, abs(Ab[i]))
        i_drag += abs(V[i]) * abs(KXP[i]) * HK
    t = KdTable(k, s, V, Ab, v_up, v_dn, a_pk, i_drag)
    _KT_CACHE[key] = t
    return t


APK_BASE = kd_table(0.5).aPk
