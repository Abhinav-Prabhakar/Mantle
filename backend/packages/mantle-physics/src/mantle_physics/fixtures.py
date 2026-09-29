"""FIXTURES ONLY: stand-ins from ``app/js/mock.js`` until field data / ML models replace them.

Nothing here is measured or learned. Each block is replaced later by data (mantle-data) or a trained
model (mantle-ml); the API marks anything sourced from here as ``source = "fixture"``.
"""

from __future__ import annotations

from typing import Any

from ._util import js_round
from .viscosity import viscosity_cp

FIXTURE_SOURCE = "fixture"

# TODO(data/M0): lab reports (L9) + Walther calibration
FLUID = {
    "api": "17–19",
    "asphaltene": 9.2,
    "tRes": 47,
    "pRes": 3.1,
    "deadOilCp": js_round(viscosity_cp(47) / 100) * 100,
}

# TODO(M4): replaced by the failure-history simulator + survival model
ROD = {
    "count": 140,
    "lengthM": 7.62,
    "tapers": [
        {"label": "1″", "to": 400},
        {"label": "⅞″", "to": 800},
        {"label": "¾″", "to": 1020},
        {"label": "sinker", "to": 1068},
    ],
    "failures": [
        {"rod": 57, "depth": 432, "size": "⅞″", "mode": "pin break at coupling", "date": "14 Mar 2026", "cause": "rod float → compressive buckling"},
        {"rod": 103, "depth": 781, "size": "¾″", "mode": "body break", "date": "2 Aug 2026", "cause": "corrosion-fatigue, high Goodman"},
    ],
    "mtbfDays": 142,
    "mtbfMantle": 260,
}

# last 12 months of pump unseat events (index 0 = oldest)
UNSEATS: dict[str, Any] = {
    "months": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    "events": [2, 5, 9],
    "holdDownKn": 18,
}

PAST_CYCLES = [{"n": 1, "k": 1.26}, {"n": 2, "k": 1.13}, {"n": 3, "k": 1.03}]

# TODO(O2): replaced by the CSS planner
PLAN = {
    "practice": {"steam": 800, "pInj": 9.0, "soak": 4, "cutoff": 120},
    "mantle": {"steam": 920, "pInj": 9.8, "soak": 6, "cutoff": 0},   # cutoff filled from the sim
    "ranges": {"steam": [500, 1200], "pInj": [7, 12], "soak": [2, 10], "cutoff": [40, 120]},
    "oilLift": 0.084,
    "sor": [3.6, 3.1],
    "inrPerCycle": 420000,
    "jointShare": 160000,
}

COST = {"maintPerDay": 6500, "chemPerDay": 1800, "steamPerT": 2800, "kwh": 8}
