"""Pydantic v2 schemas: one model per table/record type. Every record carries ``source``."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Source = Literal["real", "physics_synthetic", "llm_synthetic"]
FailureMode = Literal["fatigue", "float-buckling"]
AnomalyLabel = Literal["normal", "pump_off", "gas_lock", "load_cell_fault", "tubing_leak_onset", "vfd_trip"]
ANOMALY_LABELS: tuple[str, ...] = ("normal", "pump_off", "gas_lock", "load_cell_fault", "tubing_leak_onset", "vfd_trip")
DYNO_CLASS = Literal[
    "normal", "fluid_pound", "gas_interference", "rod_float", "pump_off", "tubing_leak",
    "travelling_valve_leak", "standing_valve_leak", "unseated_pump", "parted_rods",
    "plunger_sticking", "excessive_friction",
]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: Source


class Well(Record):  # S1
    well_id: str = Field(pattern=r"^BGW-\d{2,3}$")
    name: str
    spud_date: date
    depth_m: float = Field(gt=0)
    perf_top_m: float
    perf_bot_m: float
    net_pay_m: float = Field(gt=0)
    porosity: float = Field(gt=0, lt=1)
    perm_md: float = Field(gt=0)
    oil_saturation: float = Field(gt=0, lt=1)
    api: float = Field(ge=10, le=25)
    asphaltene_wt_pct: float = Field(gt=0)
    t_res_c: float
    p_res_mpa: float
    casing_od_in: float
    tubing_od_in: float
    rod_taper: str
    pump_bore_in: float
    pump_depth_m: float
    unit_class: str
    stroke_m: float
    vfd_kw: float
    pi_factor: float = Field(gt=0)          # productivity-index multiplier vs the showcase twin
    visc_factor: float = Field(gt=0)        # viscosity multiplier vs the showcase twin
    decline_rate: float = Field(gt=0, lt=1) # cycle-to-cycle oil multiplier decay
    steam_eff: float = Field(gt=0)          # thermal efficiency multiplier
    walther_A: float
    walther_B: float
    corrosion_index: float = Field(ge=0, le=1)
    is_showcase: bool = False


class Cycle(Record):  # S2
    well_id: str
    cycle_no: int = Field(ge=1)
    start_date: date
    steam_t: float = Field(gt=0)
    inj_pressure_mpa: float
    inj_rate_t_per_d: float
    steam_quality: float = Field(gt=0, le=1)
    soak_days: float = Field(gt=0)
    cutoff_day: int = Field(gt=0)   # last production day on the cycle timeline (planned, if in progress)
    complete: bool = True
    n_days: int = Field(gt=0)
    spm: float
    kd: float
    oil_scale: float = Field(gt=0)
    cum_oil_bbl: float = Field(ge=0)
    cum_water_bbl: float = Field(ge=0)
    sor: float = Field(ge=0)
    net_inr: float
    peak_sandface_t_c: float
    heated_radius_m: float


class CycleDaily(Record):
    well_id: str
    cycle_no: int
    day: int = Field(ge=0)
    date: date
    phase: Literal["INJECTION", "SOAK", "PRODUCTION"]
    oil_bpd: float = Field(ge=0)
    water_bpd: float = Field(ge=0)
    liquid_bpd: float = Field(ge=0)
    water_cut: float = Field(ge=0, le=1)
    sandface_t_c: float
    viscosity_cp: float = Field(gt=0)
    heated_radius_m: float
    spm_safe: float
    float_margin: float
    fillage: float = Field(ge=0, le=1)
    goodman: float = Field(ge=0)
    motor_kw: float = Field(ge=0)
    cum_oil_bbl: float = Field(ge=0)
    net_inr: float


class TelemetryRow(Record):  # S3 (stored as partitioned parquet, this is the row contract)
    ts: datetime
    well_id: str
    load_kn: float
    pos_m: float
    amps: float
    kw: float
    vfd_hz: float
    thp_mpa: float
    chp_mpa: float
    flowline_t_c: float
    label: AnomalyLabel


class DynoCard(Record):  # S4
    card_id: int
    well_id: str | None = None
    label: DYNO_CLASS
    label_idx: int = Field(ge=0, le=11)
    surface_pos: list[float] = Field(min_length=128, max_length=128)
    surface_load: list[float] = Field(min_length=128, max_length=128)
    downhole_pos: list[float] = Field(min_length=128, max_length=128)
    downhole_load: list[float] = Field(min_length=128, max_length=128)
    spm: float
    stroke_m: float
    kd: float
    fillage: float
    damping: float
    augmentation: str


class Failure(Record):  # S5
    failure_id: int
    well_id: str
    date: date
    cycle_no: int | None = None
    kind: Literal["rod_part", "tubing_leak"]
    rod_index: int | None = None
    depth_m: float | None = None
    mode: str
    goodman: float | None = None
    downtime_h: float = Field(ge=0)
    cost_inr: float = Field(ge=0)


class Unseat(Record):
    unseat_id: int
    well_id: str
    date: date
    cycle_no: int | None = None
    cycle_day: int | None = None
    uplift_kn: float
    hold_down_kn: float
    viscosity_cp: float
    downtime_h: float = Field(ge=0)
    cost_inr: float = Field(ge=0)


class Workover(Record):
    workover_id: int
    well_id: str
    date: date
    job_type: str
    trigger: Literal["rod_part", "pump_unseat", "tubing_leak", "scheduled"]
    trigger_id: int | None = None
    rig_hours: float = Field(ge=0)
    downtime_h: float = Field(ge=0)
    cost_inr: float = Field(ge=0)


class OptimiserTrace(Record):  # S6
    trace_id: int
    well_id: str | None = None
    cycle_day: float
    state_steam_t: float
    state_spm: float
    state_kd: float
    state_viscosity_cp: float
    state_sandface_t_c: float
    state_fillage: float
    state_float_margin: float
    action_spm: float
    action_kd: float
    action_steam_t: float
    action_soak_d: float
    action_cutoff_d: float
    outcome_oil_bpd: float
    outcome_kw: float
    outcome_float_margin: float
    outcome_goodman: float
    outcome_net_inr_per_day: float
    outcome_cycle_net_inr: float
    outcome_sor: float


class Weather(Record):  # R2
    ts: datetime
    temperature_c: float
    relative_humidity_pct: float
    wind_speed_kmh: float
    shortwave_wm2: float


class ViscosityLit(Record):  # R3
    sample_id: str
    api: float | None = None
    temperature_c: float
    viscosity_cp: float = Field(gt=0)
    density_g_cc: float | None = None
    citation: str
    licence: str


class ThreeWEvent(Record):  # R1 index
    instance_id: str
    event_class: int = Field(ge=0, le=9)
    event_name: str
    origin: str
    n_rows: int
    start: datetime | None = None
    end: datetime | None = None
    path: str
    licence: str = "CC BY 4.0"


# table name -> (model, primary/ordering columns)
TABLES: dict[str, type[Record]] = {
    "wells": Well, "cycles": Cycle, "cycle_daily": CycleDaily, "dyno_cards": DynoCard,
    "failures": Failure, "unseats": Unseat, "workovers": Workover, "optimiser_traces": OptimiserTrace,
    "weather": Weather, "viscosity_lit": ViscosityLit, "threew_events": ThreeWEvent,
}


def validate_frame(model: type[Record], df, sample: int | None = 500) -> int:
    """Validate (a sample of) DataFrame rows against ``model``; returns the number validated."""
    rows: list[dict[str, Any]] = df.head(sample).to_dict("records") if sample else df.to_dict("records")
    for r in rows:
        model.model_validate({k: (None if _isnan(v) else v) for k, v in r.items()})
    return len(rows)


def _isnan(v: Any) -> bool:
    try:
        return v != v  # noqa: PLR0124
    except Exception:
        return False
