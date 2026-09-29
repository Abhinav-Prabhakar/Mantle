"""Site & pumping-unit geometry (port of ``app/js/rig.js``).

Metres, +X toward the motor end, +Y up. Depth below ground is mapped to a piecewise visual scale
(``KNOTS``) so a 1.25 km well fits a 29 m pit in the 3D scene.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from ._util import JsonMixin

FACE_Z = 0.0
WELL = {"x": 0.0, "z": -1.6}

UNIT: dict[str, Any] = {
    "saddle": {"x": 5.2, "y": 6.4},
    "A": 5.2,
    "C": 3.0,
    "crank": {"x": 8.2, "y": 2.5},
    "R": 0.86,
    "P": 3.9,
    "bridle": 1.55,
    "beamLen": (-4.45, 3.4),
    "horseheadDepth": 0.95,
    "horseheadSpan": 0.34,
    "halfWidth": 1.1,
    "crankZ": 0.78,
    "skid": {"x0": 1.6, "x1": 11.4, "y0": 0.35, "y1": 0.75},
    "gearbox": {"x0": 7.35, "x1": 9.05, "y0": 0.75, "y1": 2.95, "hz": 0.52},
    "motor": {"x": 10.25, "y": 1.35, "r": 0.42, "len": 1.15},
    "stuffingBoxY": 2.05,
}


@dataclass(frozen=True)
class UnitPose(JsonMixin):
    beam: float
    crank_pin: dict
    equalizer: dict
    rope_x: float
    carrier_y: float


def unit_pose(theta: float) -> UnitPose:
    """Crank angle theta (rad) -> linkage pose, solved by bisection exactly like the JS."""
    S, C, K0, R, P, A = UNIT["saddle"], UNIT["C"], UNIT["crank"], UNIT["R"], UNIT["P"], UNIT["A"]
    kx = K0["x"] + R * math.cos(theta)
    ky = K0["y"] + R * math.sin(theta)

    def f(b: float) -> float:
        return math.hypot(S["x"] + C * math.cos(b) - kx, S["y"] + C * math.sin(b) - ky) - P

    lo, hi = -0.9, 0.9
    flo = f(lo)
    for _ in range(40):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2
    ex = S["x"] + C * math.cos(b)
    ey = S["y"] + C * math.sin(b)
    rope_top_y = S["y"]
    carrier_y = rope_top_y - UNIT["bridle"] - A * b
    return UnitPose(b, {"x": kx, "y": ky}, {"x": ex, "y": ey}, S["x"] - A, carrier_y)


@dataclass(frozen=True)
class Stroke(JsonMixin):
    bottom_y: float
    top_y: float
    length: float


def _stroke() -> Stroke:
    lo, hi = math.inf, -math.inf
    for i in range(720):
        y = unit_pose((i / 720) * math.pi * 2).carrier_y
        lo = min(lo, y)
        hi = max(hi, y)
    return Stroke(lo, hi, hi - lo)


STROKE = _stroke()


def rod_position(theta: float) -> float:
    """Polished-rod position above bottom-of-stroke (0 .. STROKE.length)."""
    return unit_pose(theta).carrier_y - STROKE.bottom_y


# ---------------------------------------------------------------- depth scale

KNOTS = [(0.0, 0.0), (30.0, -3.5), (1000.0, -16.0), (1080.0, -18.5), (1160.0, -26.0), (1250.0, -29.0)]
PIT_DEPTH = 29.0
TRUE_TD = 1250.0


def depth_to_y(d: float) -> float:
    for i in range(1, len(KNOTS)):
        if d <= KNOTS[i][0]:
            d0, y0 = KNOTS[i - 1]
            d1, y1 = KNOTS[i]
            return y0 + ((d - d0) / (d1 - d0)) * (y1 - y0)
    return KNOTS[-1][1]


def y_to_depth(y: float) -> float:
    for i in range(1, len(KNOTS)):
        if y >= KNOTS[i][1]:
            d0, y0 = KNOTS[i - 1]
            d1, y1 = KNOTS[i]
            return d0 + ((y - y0) / (y1 - y0)) * (d1 - d0)
    return KNOTS[-1][0]


STRATA = [
    {"id": "sand", "name": "Aeolian sand", "age": "Quaternary", "top": 0, "bot": 30, "color": "#d8b27a", "dark": "#b88d56", "hatch": "dots"},
    {"id": "tert", "name": "Clay & siltstone", "age": "Tertiary", "top": 30, "bot": 260, "color": "#a98a6a", "dark": "#8a6c50", "hatch": "dash"},
    {"id": "nagaur", "name": "Nagaur sandstone", "age": "Cambrian", "top": 260, "bot": 620, "color": "#b0664a", "dark": "#8c4a33", "hatch": "dots"},
    {"id": "bilara", "name": "Bilara dolomite · evaporite", "age": "Cambrian", "top": 620, "bot": 980, "color": "#9ea3a2", "dark": "#7a807f", "hatch": "brick"},
    {"id": "carb", "name": "Upper carbonate", "age": "Cambrian", "top": 980, "bot": 1080, "color": "#7d766b", "dark": "#5f5850", "hatch": "brick"},
    {"id": "jodhpur", "name": "Jodhpur sandstone · heavy oil", "age": "Neoproterozoic", "top": 1080, "bot": 1160, "color": "#6b4a2e", "dark": "#3e2a18", "hatch": "dots", "reservoir": True},
    {"id": "malani", "name": "Malani igneous suite", "age": "Basement", "top": 1160, "bot": 1250, "color": "#5a5256", "dark": "#3d373a", "hatch": "cross"},
]

WELLBORE: dict[str, Any] = {
    "casingShoe": 1175,
    "tubingBottom": 1092,
    "pumpTop": 1068,
    "pumpBottom": 1088,
    "perfTop": 1098,
    "perfBot": 1142,
    "fluidLevel": 612,
    "r": {"hole": 0.62, "casing": 0.36, "casingIn": 0.31, "tubing": 0.17, "tubingIn": 0.13, "rod": 0.045, "coupling": 0.075, "barrel": 0.2},
}

BLOCK = {"x0": -31.0, "x1": 33.0, "z0": -40.0, "depth": PIT_DEPTH}
PIT = {"x0": BLOCK["x0"], "x1": BLOCK["x1"], "depth": PIT_DEPTH, "slot": {"hw": 1.25, "z0": WELL["z"] - 1.05}}

SITE = {
    "pad": {"x0": -4.5, "x1": 13.5, "z0": -9.5, "z1": FACE_Z},
    "name": "BGW-17",
    "field": "Baghewala",
    "reservoir": "Jodhpur Sandstone",
}
