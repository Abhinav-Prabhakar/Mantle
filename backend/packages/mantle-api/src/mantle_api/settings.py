"""Configuration: genuine settings only (prices, equipment, field naming, windows). No field data lives here."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from mantle_physics.constants import PRICE, STEAM_RATE_T_PER_D

CORS_ORIGINS = ["http://localhost:8777", "http://127.0.0.1:8777", "http://localhost:8080", "http://127.0.0.1:8080"]


@dataclass(frozen=True)
class Settings:
    field_name: str = "Baghewala"
    reservoir: str = "Jodhpur Sandstone"
    showcase_well: str = "BGW-17"
    # planning prices (INR); the physics twin and O2 use the same constants
    oil_inr_bbl: float = PRICE["oil"]
    steam_inr_t: float = PRICE["steamT"]
    power_inr_kwh: float = PRICE["kwh"]
    chem_inr_day: float = 1800.0             # chemical treatment programme (demulsifier / scale inhibitor)
    # steam generator: rated output; injection days = steam volume / rate (14 d at the 800 t practice volume)
    steam_rate_t_per_d: float = STEAM_RATE_T_PER_D
    # volumetrics for the recovery factor: drainage area per well and oil formation volume factor
    drainage_area_acres: float = 6.7
    bo: float = 1.05
    failure_window_months: int = 12
    unseat_window_months: int = 12
    maint_window_days: int = 365
    live_period_s: float = 0.25
    live_sim_dt_s: float = 0.25              # simulated seconds per live message (equal to the period in production)
    live_seed: int | None = None             # sensor-noise seed (None = time-based); tests pin it
    cache_size: int = 256
    cors_origins: list[str] = field(default_factory=lambda: list(CORS_ORIGINS))

    @property
    def models_dir(self) -> Path:
        from mantle_ml import common

        return Path(os.environ.get("MANTLE_MODELS_DIR", common.models_dir()))

    @property
    def db_path(self) -> Path:
        from mantle_data.paths import db_path

        return Path(os.environ.get("MANTLE_API_DB", db_path()))


def get_settings() -> Settings:
    return Settings()
