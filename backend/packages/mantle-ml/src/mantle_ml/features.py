"""Feature tables shared by M1/M2 (and reused by M4/O2): cycle x day rows joined with cycle and well properties."""

from __future__ import annotations

import numpy as np
import pandas as pd

from mantle_physics.constants import CYCLE_DAYS, INJ_END, SOAK_END, T_RES

from . import fasttwin as ft

WELL_COLS = ["well_id", "steam_eff", "pi_factor", "visc_factor", "decline_rate", "api", "asphaltene_wt_pct",
             "walther_A", "walther_B", "corrosion_index", "rod_stress_factor"]
CYCLE_COLS = ["well_id", "cycle_no", "steam_t", "inj_pressure_mpa", "steam_quality", "soak_days", "spm", "kd",
              "cutoff_day", "complete", "cum_oil_bbl"]
PHASE = {"INJECTION": 0, "SOAK": 1, "PRODUCTION": 2}


def twin_day(a, soak):
    """Actual cycle day -> twin day axis (mirrors ``synth.s2_cycles.twin_day``)."""
    a = np.asarray(a, dtype=float)
    a_p = INJ_END + soak
    base = SOAK_END - INJ_END
    return np.where(a < INJ_END, a, np.where(a < a_p, INJ_END + (a - INJ_END) * base / soak, SOAK_END + (a - a_p)))


def analytic_thermal(steam, day, steam_eff=1.0):
    """Pure analytic (Marx-Langenheim/Boberg-Lantz twin law) T, r_h, excess at actual ``day`` (no soak remap)."""
    steam = np.asarray(steam, dtype=float)
    d = np.clip(np.asarray(day, dtype=float), 0, CYCLE_DAYS)
    i0 = np.clip(np.floor(d).astype(int), 0, CYCLE_DAYS - 1)
    f = d - i0
    b = ft.base_at(ft.eff_steam(steam, steam_eff) if np.any(np.asarray(steam_eff) != 1.0) else steam)
    T = ft.base_field(b, "T")
    rh = ft.base_field(b, "rh")
    ex = ft.base_field(b, "exc")
    if b.ndim == 2:
        return tuple(x[i0] * (1 - f) + x[i0 + 1] * f for x in (T, rh, ex))
    ar = np.arange(len(i0))
    return tuple(x[ar, i0] * (1 - f) + x[ar, i0 + 1] * f for x in (T, rh, ex))


def daily_table(cycles: pd.DataFrame, daily: pd.DataFrame, wells: pd.DataFrame) -> pd.DataFrame:
    df = daily.merge(cycles[CYCLE_COLS], on=["well_id", "cycle_no"]).merge(wells[WELL_COLS], on="well_id")
    df["phase_i"] = df["phase"].map(PHASE)
    df["a_p"] = INJ_END + df["soak_days"]
    df["dprod"] = df["day"] - df["a_p"]                       # days since production start (may be < 0)
    T, rh, ex = analytic_thermal(df["steam_t"].to_numpy(), df["day"].to_numpy())
    df["an_T"], df["an_rh"], df["an_exc"] = T, rh, ex
    Te, rhe, exe = analytic_thermal(df["steam_t"].to_numpy(), df["day"].to_numpy(), df["steam_eff"].to_numpy())
    df["an_Te"], df["an_rhe"], df["an_exce"] = Te, rhe, exe
    # per-cycle peak excess -> thermal battery target
    peak = df.groupby(["well_id", "cycle_no"])["sandface_t_c"].transform("max") - T_RES
    df["battery"] = np.clip((df["sandface_t_c"] - T_RES) / peak.clip(lower=1e-6), 0, 1)
    return df


def group_folds(well_ids: pd.Series, n_splits: int, seed: int = 0) -> np.ndarray:
    """Deterministic fold index per row, grouped by well (no well appears in two folds)."""
    ids = sorted(well_ids.unique())
    r = np.random.default_rng(seed)
    perm = r.permutation(len(ids))
    fold_of = {ids[i]: k % n_splits for k, i in enumerate(perm)}
    return well_ids.map(fold_of).to_numpy()
