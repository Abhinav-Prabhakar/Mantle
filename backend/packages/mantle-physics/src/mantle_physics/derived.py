"""``derive(metrics, state)``: port of ``mock.js`` ``derive()``.

Values are computed from live twin state where that moves plausibly and from fixtures otherwise
(see :mod:`mantle_physics.fixtures`). The hazard-based replacements live in :mod:`mantle_physics.hazard`.
"""

from __future__ import annotations

import math
from typing import Any

from ._util import clamp
from .constants import CYCLE_DAYS, SOAK_END
from .fixtures import COST, FLUID, UNSEATS
from .twin import Metrics, State


def derive(m: Metrics, st: State | None = None) -> dict[str, Any]:
    """Return the derived (mock) fields with the exact camelCase keys the frontend consumes."""
    prod = m.phase == "PRODUCTION"
    spm = st.spm_actual if st is not None else m.spm
    hz = spm * 50 / 9
    amps_avg = (m.motor_kw * 1000) / (1.732 * 415 * 0.86) if prod else 0.0
    load = st.load if st is not None else m.pprl
    load_frac = clamp(load / m.pprl, 0, 1.2) if m.pprl > 0 else 0.0
    amps = amps_avg * (0.55 + 0.9 * load_frac) if prod else 0.0
    profile = []
    for i in range(36):
        th = (i / 35) * math.pi * 2
        profile.append(1 + (m.kd - 0.5) * 0.9 * math.cos(th) + 0.05 * math.sin(2 * th))

    thp = 0.55 + m.oil_rate * 0.004 if prod else 9.4 if m.phase == "INJECTION" else 2.8
    chp = 0.28 if prod else 0.4 if m.phase == "INJECTION" else 1.9
    pip = 0.2 + m.submergence * 0.0091
    flow_t = 40 + (m.sandface_t - 47) * 0.45 if prod else 285.0 if m.phase == "INJECTION" else 60.0

    def pound(fill: float) -> float:
        return clamp((0.85 - fill) / 0.35, 0, 1)

    impacts_day = spm * 1440 * pound(m.fillage) if prod else 0.0
    rec = m.recommendation
    fill2 = clamp(m.fillage * m.spm / max(rec.spm, 0.5), 0, 0.97)
    impacts_mantle = rec.spm * 1440 * pound(fill2) if prod else 0.0
    impact_vel = (0.15 + (1 - m.fillage) * 1.3) * spm / 5.4 if prod else 0.0

    uplift = 9 + (m.viscosity / 1000) * 2.5 + (1 - m.fillage) * 8
    uplift_margin = UNSEATS["holdDownKn"] / uplift
    unseat_risk = clamp(0.05 + (2.0 - uplift_margin) * 0.3, 0.03, 0.7)

    prod_days = CYCLE_DAYS - SOAK_END
    steam_day = (COST["steamPerT"] * m.steam_tons) / prod_days
    power_day = m.motor_kw * 24 * COST["kwh"]
    cost_day = steam_day + power_day + COST["maintPerDay"] + COST["chemPerDay"]
    cost_bbl = cost_day / m.oil_rate if prod and m.oil_rate > 0.5 else None

    past_cum = 3900 + 3500 + 3150
    recovery = (past_cum + m.cum_oil) / 1.2e6

    return {
        "hz": hz, "amps": amps, "ampsAvg": amps_avg, "profile": profile, "stroke": m.stroke,
        "thp": thp, "chp": chp, "pip": pip, "flowT": flow_t, "pRes": FLUID["pRes"],
        "counterbalance": clamp(0.97 - abs(m.kd - 0.52) * 0.25, 0.7, 1), "beamLoad": m.pprl / 120,
        "impactsDay": impacts_day, "impactsMantle": impacts_mantle, "impactVel": impact_vel,
        "uplift": uplift, "upliftMargin": uplift_margin, "unseatRisk": unseat_risk,
        "cost": {
            "steamDay": steam_day, "powerDay": power_day, "maintDay": COST["maintPerDay"],
            "chemDay": COST["chemPerDay"], "costDay": cost_day, "costBbl": cost_bbl,
        },
        "recovery": recovery,
    }
