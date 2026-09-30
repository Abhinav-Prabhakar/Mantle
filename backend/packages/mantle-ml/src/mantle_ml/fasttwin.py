"""Vectorised, interpolated copy of the twin's per-day core for optimisers and surrogates.

``mantle_physics.pump.core`` is exact but scalar (~30 us/call). The optimisers (O1/O2/O3) need thousands of
evaluations per second, so this module tabulates the twin's production base state (``prod_base``) on a steam
grid and the kd stroke-shaping constants on a kd grid, interpolates linearly, and evaluates the same equations
with numpy broadcasting. ``tests/ml`` pins it to the scalar twin (parity within ~1 %).
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

import numpy as np

from mantle_physics.constants import (
    CYCLE_DAYS,
    ETA_S,
    FRIC_FRAC,
    LBF_N,
    OIL_SG,
    PLUNGER_IN,
    PRICE,
    PUMP_DEPTH,
    S_IN,
    S_M,
    SOAK_END,
    SPM_MAX,
    TAU,
    TORQUE_RATING_INLB,
    WATER_SG,
)
from mantle_physics.pump import PD_K
from mantle_physics.reservoir import prod_base
from mantle_physics.rods import APK_BASE, SECT, W_R, kd_table, w_below

STEAMS = np.arange(300.0, 1401.0, 25.0)
KDS = np.round(np.arange(0.40, 0.7001, 0.01), 3)
BASE_FIELDS = ("qIn", "wc", "c", "c500", "c800", "muPump", "T", "exc", "rh", "Lr")
_NB = len(BASE_FIELDS)
DAYS = np.arange(CYCLE_DAYS + 1)
_SECT_A = {0: SECT[0].A, 500: SECT[1].A, 800: SECT[2].A}
_WB = {x: w_below(x) for x in (0, 500, 800)}


def build_tables() -> dict[str, np.ndarray]:
    base = np.zeros((len(STEAMS), CYCLE_DAYS + 1, _NB))
    for i, s in enumerate(STEAMS):
        for d in DAYS:
            b = prod_base(float(s), float(d))
            base[i, d] = [b.qIn, b.wc, b.c, b.c500, b.c800, b.muPump, b.T, b.th.exc, b.rh, b.Lr]
    kd = np.zeros((len(KDS), 4))
    for i, k in enumerate(KDS):
        t = kd_table(float(k))
        kd[i] = [t.vUp, t.vDn, t.aPk, t.iDrag]
    return {"base": base, "kd": kd, "steams": STEAMS, "kds": KDS}


_TABLES: dict[str, np.ndarray] | None = None


def default_path() -> Path:
    from .common import models_dir

    return models_dir() / "_twin" / "grid.npz"


def tables() -> dict[str, np.ndarray]:
    """Lazy-loaded grid tables (from ``models/_twin/grid.npz`` if present, else computed in ~2 s)."""
    global _TABLES
    if _TABLES is None:
        p = default_path()
        if p.exists():
            z = np.load(p)
            _TABLES = {k: z[k] for k in z.files}
        else:
            _TABLES = build_tables()
    return _TABLES


def save_tables(path: Path | None = None) -> Path:
    p = path or default_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(p, **build_tables())  # type: ignore[arg-type]
    return p


def base_at(steam) -> np.ndarray:
    """Base state fields interpolated at ``steam`` (t): shape ``(*steam.shape, 121, n_fields)``."""
    t = tables()
    s = np.clip(np.asarray(steam, dtype=float), STEAMS[0], STEAMS[-1])
    pos = (s - STEAMS[0]) / (STEAMS[1] - STEAMS[0])
    i0 = np.clip(np.floor(pos).astype(int), 0, len(STEAMS) - 2)
    f = (pos - i0)[..., None, None]
    b = t["base"]
    return b[i0] * (1 - f) + b[i0 + 1] * f


def base_field(b: np.ndarray, name: str) -> np.ndarray:
    return b[..., BASE_FIELDS.index(name)]


def kd_consts(kd) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(vUp, vDn, aPk, iDrag) interpolated over kd."""
    t = tables()
    k = np.clip(np.asarray(kd, dtype=float), KDS[0], KDS[-1])
    return tuple(np.interp(k, t["kds"], t["kd"][:, j]) for j in range(4))


def _softmin(a, b, p: float = 10.0):
    return (np.maximum(a, 1e-6) ** -p + np.maximum(b, 1e-6) ** -p) ** (-1 / p)


def core(qIn, wc, c, c500, c800, spm, kd, k_oil=1.0) -> dict[str, np.ndarray]:
    """Vectorised ``mantle_physics.pump.core``; all arguments broadcast. ``k_oil`` is the per-well productivity
    multiplier applied like ``synth.wellmodel`` does (oil/liquid linear, fillage ** 0.6)."""
    vUp_k, vDn_k, aPk, iDrag = kd_consts(kd)
    Gfl = (1 - wc) * OIL_SG + wc * WATER_SG
    bf = 1 - 0.128 * Gfl
    Wrf = W_R * bf
    Fo = 0.340 * Gfl * PLUNGER_IN**2 * (PUMP_DEPTH / 0.3048) * LBF_N
    omega = TAU * spm / 60
    vUp, vDn = omega * vUp_k, omega * vDn_k
    dUp, dDn = c * vUp, c * vDn
    Ffric = FRIC_FRAC * Wrf
    margin_raw = 1 - (dDn + Ffric) / Wrf
    k_safe = np.maximum(c * (TAU / 60) * vDn_k, 1e-12)
    spm_safe = np.clip((0.85 * Wrf - Ffric) / k_safe, 0.5, SPM_MAX)
    eta_float = 1 - np.clip(-margin_raw * 0.8, 0, 0.5)
    PDg = PD_K * spm
    PDe = np.maximum(1e-6, PDg * ETA_S * eta_float)
    q = _softmin(qIn, PDe)
    fill = np.clip(q / PDe, 0, 0.98)
    alpha = (S_IN * spm**2 / 70500) * (aPk / APK_BASE)
    pprl = (Wrf + Fo + W_R * alpha + dUp) / 1000
    mprl = np.maximum(0.0, (Wrf - W_R * alpha - dDn) / 1000)
    torque = np.clip(0.25 * S_IN * ((pprl - mprl) * 1000 / LBF_N) * 0.55 / TORQUE_RATING_INLB, 0, 1.5)
    gm = 0.0
    for X, cb in ((0, c), (500, c500), (800, c800)):
        wb, A = _WB[X], _SECT_A[X]
        smax = (wb * bf + Fo + wb * alpha + cb * vUp) / A
        smin = np.maximum(0.0, (wb * bf - wb * alpha - cb * vDn) / A)
        gm = np.maximum(gm, smax / (0.85 * (793 / 4 + 0.5625 * smin)))
    goodman = np.clip(gm, 0, 1.5)
    work = Fo * S_M * fill + c * omega * iDrag
    motor_kw = work * spm / 60 / 1000 / (0.85 * 0.9) + 0.5
    oil = q * (1 - wc)
    if not (np.isscalar(k_oil) and k_oil == 1.0):
        oil, liq = oil * k_oil, q * k_oil
        fill = np.minimum(0.98, fill * np.asarray(k_oil) ** 0.6)
    else:
        liq = q
    return {
        "oil": oil, "liquid": liq, "fill": fill, "margin_raw": margin_raw,
        "margin": np.clip(margin_raw, -1, 1), "spm_safe": spm_safe, "goodman": goodman,
        "torque": torque, "kw": motor_kw, "pprl": pprl, "mprl": mprl, "vUp": vUp, "q": q,
        "pump_limited": qIn > PDe,
    }


def eff_steam(steam, steam_eff: float = 1.0):
    return np.clip(np.round(np.asarray(steam) * steam_eff), 300, 1400)


def cycle_days(steam, spm, kd, *, steam_eff: float = 1.0, k_oil: float = 1.0, visc_factor: float = 1.0):
    """Twin-day arrays (0..120) for one (steam, spm, kd), like ``wellmodel.cycle_run`` but interpolated."""
    b = base_at(eff_steam(steam, steam_eff))
    f = {n: base_field(b, n) for n in BASE_FIELDS}
    prod = DAYS >= SOAK_END
    bb = np.where(prod, 1, 0)
    def pick(a):
        return np.where(prod, a, a[SOAK_END])

    r = core(pick(f["qIn"]), pick(f["wc"]), pick(f["c"]), pick(f["c500"]), pick(f["c800"]), spm, kd, k_oil)
    out = {k: np.where(prod, v, 0.0) if k in ("oil", "liquid", "fill", "kw") else v for k, v in r.items() if k != "pump_limited"}
    out["T"], out["rh"], out["mu"] = f["T"], f["rh"], f["muPump"] * visc_factor
    out["wc"] = np.where(prod, f["wc"], 0.0)
    out["water"] = out["liquid"] * out["wc"]
    del bb
    return out


def value_per_day(oil, kw, oil_price: float = PRICE["oil"], kwh_price: float = PRICE["kwh"]):
    return oil * oil_price - kw * 24 * kwh_price


@lru_cache(maxsize=1)
def _noop() -> None:  # pragma: no cover
    return None


def pound(fill):
    return np.clip((0.85 - np.asarray(fill)) / 0.35, 0, 1)


def hz_of(spm):
    return np.asarray(spm) * 50 / 9


assert math.isclose(TAU, 2 * math.pi)
