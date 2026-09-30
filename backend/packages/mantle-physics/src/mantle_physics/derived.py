"""``derive(metrics, state, ctx)``: quantities the UI shows that follow from the twin state.

Two groups:

* **Physical** (always returned): VFD Hz, motor amps, the speed-across-stroke profile, wellhead pressures,
  pump-intake pressure, flowline temperature, counterbalance, beam load and the fluid-pound impact laws. These
  are deterministic functions of the twin state (the S3 telemetry generator uses the same ones).
* **Well-specific** (returned when a :class:`WellContext` is supplied): reservoir pressure, the uplift force on
  the pump and its margin against the hold-down, the daily cost anatomy and the recovery factor. Every input of
  a :class:`WellContext` comes from the well master, the recorded workovers/cycles or the price settings; there
  are no built-in defaults, so nothing here can fall back to a stand-in value.

The hazard-based / ML refinements (impacts from M5, unseat risk from M4) are applied by the API layer.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from ._util import clamp
from .constants import CYCLE_DAYS, S_M, SOAK_END
from .hazard import pump_uplift_kn
from .twin import Metrics, State


@dataclass(frozen=True)
class WellContext:
    """Everything ``derive`` needs to know about one well that the twin itself does not model."""

    p_res_mpa: float              # reservoir pressure (well master)
    hold_down_kn: float           # pump hold-down capacity (well master)
    steam_inr_per_t: float        # price settings
    power_inr_per_kwh: float
    oil_inr_per_bbl: float
    maint_inr_per_day: float      # trailing-year recorded workover cost / 365 (S5)
    chem_inr_per_day: float       # chemical treatment programme (settings)
    past_cum_oil_bbl: float       # cumulative oil of the completed cycles (S2)
    ooip_bbl: float               # drainage-area OOIP (well master petrophysics)


def pound(fill: float) -> float:
    return clamp((0.85 - fill) / 0.35, 0, 1)


def derive(m: Metrics, st: State | None = None, ctx: WellContext | None = None) -> dict[str, Any]:
    """Return the derived fields with the exact camelCase keys the frontend consumes."""
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

    impacts_day = spm * 1440 * pound(m.fillage) if prod else 0.0
    rec = m.recommendation
    fill2 = clamp(m.fillage * m.spm / max(rec.spm, 0.5), 0, 0.97)
    impacts_mantle = rec.spm * 1440 * pound(fill2) if prod else 0.0
    impact_vel = (0.15 + (1 - m.fillage) * 1.3) * spm / 5.4 if prod else 0.0

    out: dict[str, Any] = {
        "hz": hz, "amps": amps, "ampsAvg": amps_avg, "profile": profile, "stroke": m.stroke,
        "thp": thp, "chp": chp, "pip": pip, "flowT": flow_t,
        "counterbalance": clamp(0.97 - abs(m.kd - 0.52) * 0.25, 0.7, 1), "beamLoad": m.pprl / 120,
        "impactsDay": impacts_day, "impactsMantle": impacts_mantle, "impactVel": impact_vel,
    }
    if ctx is None:
        return out

    v_up = math.pi * S_M * m.spm / 60
    uplift = float(pump_uplift_kn(m.viscosity, v_up, m.fillage if prod else 1.0))
    uplift_margin = ctx.hold_down_kn / uplift
    unseat_risk = clamp(0.05 + (2.0 - uplift_margin) * 0.3, 0.03, 0.7)     # replaced by M4 in the API
    prod_days = CYCLE_DAYS - SOAK_END
    steam_day = ctx.steam_inr_per_t * m.steam_tons / prod_days
    power_day = m.motor_kw * 24 * ctx.power_inr_per_kwh
    cost_day = steam_day + power_day + ctx.maint_inr_per_day + ctx.chem_inr_per_day
    cost_bbl = cost_day / m.oil_rate if prod and m.oil_rate > 0.5 else None
    out.update({
        "pRes": ctx.p_res_mpa, "uplift": uplift, "upliftMargin": uplift_margin, "unseatRisk": unseat_risk,
        "cost": {
            "steamDay": steam_day, "powerDay": power_day, "maintDay": ctx.maint_inr_per_day,
            "chemDay": ctx.chem_inr_per_day, "costDay": cost_day, "costBbl": cost_bbl,
            "revenueDay": m.oil_rate * ctx.oil_inr_per_bbl if prod else 0.0,
        },
        "recovery": (ctx.past_cum_oil_bbl + m.cum_oil) / ctx.ooip_bbl,
    })
    return out
