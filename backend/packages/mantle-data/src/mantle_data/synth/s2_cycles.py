"""S2: CSS cycle histories (cycles table + daily rows) from the twin scaled per well."""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from mantle_physics.constants import CYCLE_DAYS, INJ_END, PRICE, SOAK_END

from .common import SEED, SHOWCASE_ID, SOURCE, Scale, get_scale, rng_for
from .wellmodel import BASE_SOAK_DAYS, CycleRun, best_cutoff, cycle_run

AS_OF = date(2026, 9, 30)
SHOWCASE_CYCLE_DAY = 41
SHOWCASE_PAST_CUM = (3900.0, 3500.0, 3150.0)        # from the frontend fixtures (bbl per past cycle)
DAILY_COLS = [
    "well_id", "cycle_no", "day", "date", "phase", "oil_bpd", "water_bpd", "liquid_bpd", "water_cut",
    "sandface_t_c", "viscosity_cp", "heated_radius_m", "spm_safe", "float_margin", "fillage", "goodman",
    "motor_kw", "cum_oil_bbl", "net_inr", "source",
]


def twin_day(a: np.ndarray, soak: float) -> np.ndarray:
    """Map actual cycle day (injection 0..13, soak, production) onto the twin's 0..120 axis."""
    a = np.asarray(a, dtype=float)
    a_p = INJ_END + soak
    return np.where(a < INJ_END, a, np.where(a < a_p, INJ_END + (a - INJ_END) * BASE_SOAK_DAYS / soak,
                                             SOAK_END + (a - a_p)))


def build_cycle(well: dict, cycle_no: int, start: date, p: dict, last_day: int | None = None
                ) -> tuple[dict, pd.DataFrame]:
    """One cycle. ``last_day`` (actual day index) truncates an in-progress cycle."""
    steam, soak = p["steam_t"], p["soak_days"]
    run: CycleRun = cycle_run(steam, p["spm"], p["kd"], steam_eff=well["steam_eff"],
                              oil_scale=p["oil_scale"], visc_factor=well["visc_factor"], soak_days=soak)
    cutoff_twin = int(p["cutoff_twin"])
    a_p = INJ_END + soak
    planned_last = int(round(a_p + (cutoff_twin - SOAK_END)))
    complete = last_day is None
    last = planned_last if complete else min(last_day, planned_last)
    a = np.arange(0, last + 1)
    d = twin_day(a, soak)
    ax = np.arange(CYCLE_DAYS + 1)

    def at(arr: np.ndarray) -> np.ndarray:
        return np.interp(d, ax, arr)

    phase = np.where(a < INJ_END, "INJECTION", np.where(a < a_p, "SOAK", "PRODUCTION"))
    prod = phase == "PRODUCTION"
    oil = np.where(prod, at(run.oil), 0.0)
    water = np.where(prod, at(run.water), 0.0)
    liquid = np.where(prod, at(run.liquid), 0.0)
    kw = np.where(prod, at(run.kw), 0.0)
    net = np.where(prod, oil * PRICE["oil"] - kw * 24 * PRICE["kwh"],
                   np.where(a < INJ_END, -(steam / INJ_END) * PRICE["steamT"], 0.0))
    df = pd.DataFrame({
        "well_id": well["well_id"], "cycle_no": cycle_no, "day": a,
        "date": [start + timedelta(days=int(x)) for x in a], "phase": phase,
        "oil_bpd": oil, "water_bpd": water, "liquid_bpd": liquid,
        "water_cut": np.where(prod, at(run.wc), 0.0), "sandface_t_c": at(run.T),
        "viscosity_cp": np.maximum(at(run.mu), 0.3), "heated_radius_m": at(run.rh),
        "spm_safe": at(run.spm_safe), "float_margin": at(run.margin),
        "fillage": np.where(prod, at(run.fill), 0.0), "goodman": at(run.goodman),
        "motor_kw": kw, "cum_oil_bbl": np.cumsum(oil), "net_inr": net, "source": SOURCE,
    })
    cum_oil, cum_w = float(oil.sum()), float(water.sum())
    from mantle_physics.economics import sor as sor_fn

    row = {
        "well_id": well["well_id"], "cycle_no": cycle_no, "start_date": start, "steam_t": float(steam),
        "inj_pressure_mpa": p["p_inj"], "inj_rate_t_per_d": float(steam) / INJ_END,
        "steam_quality": p["quality"], "soak_days": float(soak), "cutoff_day": planned_last,
        "complete": complete, "n_days": int(len(a)), "spm": p["spm"], "kd": p["kd"],
        "oil_scale": p["oil_scale"], "cum_oil_bbl": cum_oil, "cum_water_bbl": cum_w,
        "sor": float(sor_fn(steam, cum_oil)), "net_inr": float(net.sum()),
        "peak_sandface_t_c": float(df["sandface_t_c"].max()),
        "heated_radius_m": float(df["heated_radius_m"].max()), "source": SOURCE,
    }
    return row, df


def _sample_params(rng: np.random.Generator, well: dict, n: int) -> dict:
    steam = float(np.clip(rng.normal(820 + 8 * n, 110), 500, 1200))
    spm = float(rng.uniform(4.0, 7.2))
    kd = float(rng.choice([0.46, 0.5, 0.54, 0.58, 0.62]))
    soak = float(rng.integers(3, 11))
    run = cycle_run(steam, spm, kd, steam_eff=well["steam_eff"], oil_scale=well["pi_factor"], soak_days=soak)
    if rng.random() < 0.6:      # a well-managed cycle: the operator matches pump speed to inflow
        for _ in range(3):
            fill = run.fill[SOAK_END + 5: SOAK_END + 60].mean()
            spm = float(np.clip(spm * (fill / 0.88) ** 1.6, 1.6, 7.2))
            run = cycle_run(steam, spm, kd, steam_eff=well["steam_eff"], oil_scale=well["pi_factor"],
                            soak_days=soak)
    cutoff = int(np.clip(best_cutoff(run, steam) + rng.normal(0, 10), 60, CYCLE_DAYS))
    oil_scale = well["pi_factor"] * well["decline_rate"] ** (n - 1) * float(np.exp(rng.normal(0, 0.06)))
    return {
        "steam_t": round(steam), "spm": round(spm, 2), "kd": kd, "soak_days": soak, "cutoff_twin": cutoff,
        "p_inj": float(np.clip(7 + (steam - 500) / 700 * 5 + rng.normal(0, 0.4), 7, 12)),
        "quality": float(rng.uniform(0.62, 0.80)), "oil_scale": oil_scale,
    }


def _showcase(well: dict) -> tuple[list[dict], list[pd.DataFrame]]:
    start = AS_OF - timedelta(days=SHOWCASE_CYCLE_DAY)
    out_rows, out_dfs = [], []
    cur = {"steam_t": 800, "spm": 5.4, "kd": 0.5, "soak_days": float(BASE_SOAK_DAYS), "cutoff_twin": 0,
           "p_inj": 9.0, "quality": 0.72, "oil_scale": 1.0}
    cur["cutoff_twin"] = best_cutoff(cycle_run(800, 5.4, 0.5), 800)
    # past cycles: solve oil_scale to hit the frontend's cumulative-oil fixtures
    ends = start - timedelta(days=21)
    plans = []
    for k, target in zip(range(3, 0, -1), SHOWCASE_PAST_CUM[::-1], strict=True):
        p = {"steam_t": 800, "spm": 5.4, "kd": 0.5, "soak_days": float(BASE_SOAK_DAYS), "p_inj": 9.0,
             "quality": 0.72, "cutoff_twin": 110 - 6 * (3 - k)}
        base = cycle_run(800, 5.4, 0.5)
        unit = float(np.sum(base.oil[SOAK_END: p["cutoff_twin"] + 1]))
        p["oil_scale"] = target / unit
        plans.append((k, p))
    for k, p in plans:    # k=3 first: go backwards from the current cycle
        n_days = int(INJ_END + BASE_SOAK_DAYS + p["cutoff_twin"] - SOAK_END) + 1
        s = ends - timedelta(days=n_days)
        row, df = build_cycle(well, k, s, p)
        out_rows.append(row)
        out_dfs.append(df)
        ends = s - timedelta(days=21)
    row, df = build_cycle(well, 4, start, cur, last_day=SHOWCASE_CYCLE_DAY)
    out_rows.append(row)
    out_dfs.append(df)
    return out_rows, out_dfs


def generate(wells: pd.DataFrame, scale: str | Scale = "default", seed: int = SEED
             ) -> tuple[pd.DataFrame, pd.DataFrame]:
    sc = get_scale(scale)
    ids = list(wells["well_id"])
    chosen = [SHOWCASE_ID] + [w for w in ids if w != SHOWCASE_ID]
    chosen = chosen[: sc.cycle_wells]
    rows: list[dict] = []
    dfs: list[pd.DataFrame] = []
    for wid in sorted(chosen):
        well = wells[wells.well_id == wid].iloc[0].to_dict()
        if wid == SHOWCASE_ID:
            r, d = _showcase(well)
            rows += r
            dfs += d
            continue
        rng = rng_for(seed, "S2", int(wid.split("-")[1]))
        n_done = int(rng.integers(sc.cycles[0], sc.cycles[1] + 1))
        cur_day = int(rng.integers(8, 100))
        cur_start = AS_OF - timedelta(days=cur_day)
        # plan completed cycles going backwards, dropping any that would start before spud + 180 d
        earliest = well["spud_date"] + timedelta(days=180)
        built = []
        end = cur_start - timedelta(days=int(rng.integers(7, 30)))
        for k in range(n_done, 0, -1):
            p = _sample_params(rng, well, k)
            n_days = int(INJ_END + p["soak_days"] + p["cutoff_twin"] - SOAK_END) + 1
            s = end - timedelta(days=n_days)
            if s < earliest:
                break
            built.append((k, s, p))
            end = s - timedelta(days=int(rng.integers(7, 30)))
        built.reverse()
        # renumber so the earliest kept cycle is cycle 1
        for i, (_, s, p) in enumerate(built, start=1):
            p["oil_scale"] = well["pi_factor"] * well["decline_rate"] ** (i - 1) * float(np.exp(rng.normal(0, 0.06)))
            r, d = build_cycle(well, i, s, p)
            rows.append(r)
            dfs.append(d)
        p = _sample_params(rng, well, len(built) + 1)
        p["oil_scale"] = well["pi_factor"] * well["decline_rate"] ** len(built)
        r, d = build_cycle(well, len(built) + 1, cur_start, p, last_day=cur_day)
        rows.append(r)
        dfs.append(d)
    cycles = pd.DataFrame(rows).sort_values(["well_id", "cycle_no"]).reset_index(drop=True)
    daily = pd.concat(dfs, ignore_index=True)[DAILY_COLS]
    daily = daily.sort_values(["well_id", "cycle_no", "day"]).reset_index(drop=True)
    return cycles, daily
