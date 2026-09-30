"""Walther / ASTM D341 viscosity law fitted through 12,000 cP @ 50 C and 80 cP @ 150 C."""

from __future__ import annotations

import math

from ._util import clamp, fin
from .constants import T_RES


def _fit() -> tuple[float, float]:
    def f(cp: float, c: float) -> tuple[float, float]:
        return math.log10(math.log10(cp / 0.96 + 0.7)), math.log10(c + 273.15)

    y1, x1 = f(12000, 50)
    y2, x2 = f(80, 150)
    B = (y1 - y2) / (x2 - x1)
    return y1 + B * x1, B


WAL_A, WAL_B = _fit()


def viscosity_cp(t_c: float) -> float:
    """Dead-oil viscosity (cP) at temperature ``t_c`` (C); clamped to 5..320 C, floor 0.3 cP."""
    T = clamp(fin(t_c, T_RES), 5, 320)
    nu = math.pow(10, math.pow(10, WAL_A - WAL_B * math.log10(T + 273.15))) - 0.7
    return max(0.3, nu * 0.96)


MU_COLD = viscosity_cp(T_RES)
