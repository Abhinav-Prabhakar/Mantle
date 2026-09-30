"""S5: rod-part / unseat / tubing-leak histories and workovers, from ``mantle_physics.hazard`` over S2."""

from __future__ import annotations

import zlib
from datetime import timedelta

import numpy as np
import pandas as pd

from mantle_physics import WellSim, pump_unseat_hazard, pump_uplift_kn, simulate_rod_failures
from mantle_physics.constants import INJ_END, S_M
from mantle_physics.hazard import N_RODS, ROD_LENGTH_M

from .common import SEED, SOURCE, rng_for

RIG_INR_PER_H = 11_000.0
ROD_MATERIAL_INR = 8_000.0
TUBING_LEAK_HAZARD = 6e-4     # per production day at corrosion index 1


def _rod_goodman(peak: float, spm: float, kd: float, steam: float, day: float) -> np.ndarray:
    """Per-rod Goodman ratio: cycle-peak Goodman scaled by the twin's stress-vs-depth profile."""
    prof = WellSim(spm=spm, cycle_day=min(max(day, 19), 120), kd=kd, steam=steam).profile()
    depth = np.array(prof.depth)
    stress = np.array(prof.rod_stress)
    z = (np.arange(N_RODS) + 0.5) * ROD_LENGTH_M
    s = np.interp(z, depth, stress)
    top = max(float(stress[depth < 1068].max()), 1e-9)
    return peak * np.clip(s / top, 0, 1)


def conditions(rows: pd.DataFrame, cyc: dict) -> dict | None:
    """Mean production-period conditions of one cycle from its daily rows."""
    p = rows[rows.phase == "PRODUCTION"]
    if len(p) < 2:
        return None
    spm = float(cyc["spm"])
    fill = p["fillage"].to_numpy()
    pound = np.clip((0.85 - fill) / 0.35, 0, 1)
    margin = p["float_margin"].to_numpy()
    return {
        "days": len(p), "goodman": float(p["goodman"].mean()), "spm": spm,
        "float_frac": float(np.clip((0.15 - margin) / 0.3, 0, 1).mean()),
        "impacts": float((spm * 1440 * pound).mean()),
        "impact_vel": float(((0.15 + (1 - fill) * 1.3) * spm / 5.4).mean()),
        "mid_day": float(p["day"].iloc[len(p) // 2]),
    }


def generate(wells: pd.DataFrame, cycles: pd.DataFrame, daily: pd.DataFrame, seed: int = SEED
             ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fail, uns, work = [], [], []
    fid = uid = wid_ = 0
    well_idx = wells.set_index("well_id")
    for wid, gc in cycles.groupby("well_id"):
        well = well_idx.loc[wid]
        rng = rng_for(seed, "S5", int(wid.split("-")[1]))
        hold_down = 26.0 * (0.85 + 0.3 * (zlib.crc32(wid.encode()) % 100) / 100)
        for cyc in gc.to_dict("records"):
            rows = daily[(daily.well_id == wid) & (daily.cycle_no == cyc["cycle_no"])]
            cond = conditions(rows, cyc)
            if cond is None:
                continue
            a_p = INJ_END + cyc["soak_days"]
            start = cyc["start_date"]
            n_prod = cond["days"]
            gr = float(well["rod_stress_factor"]) * _rod_goodman(cond["goodman"], cyc["spm"], cyc["kd"], cyc["steam_t"], cond["mid_day"])
            for f in simulate_rod_failures(
                rng, gr, cond["spm"] * 1440, n_prod, cond["float_frac"], cond["impacts"], cond["impact_vel"],
                float(well["corrosion_index"]),
            ):
                fid += 1
                wid_ += 1
                rig_h = float(rng.uniform(18, 60))
                down = rig_h + float(rng.uniform(6, 30))
                cost = rig_h * RIG_INR_PER_H + 2 * ROD_MATERIAL_INR
                d = start + timedelta(days=int(a_p + f.day))
                fail.append({"failure_id": fid, "well_id": wid, "date": d, "cycle_no": cyc["cycle_no"],
                             "kind": "rod_part", "rod_index": f.rod, "depth_m": f.depth_m, "mode": f.mode,
                             "goodman": f.goodman, "downtime_h": down, "cost_inr": cost, "source": SOURCE})
                work.append({"workover_id": wid_, "well_id": wid, "date": d, "job_type": "rod job",
                             "trigger": "rod_part", "trigger_id": fid, "rig_hours": rig_h, "downtime_h": down,
                             "cost_inr": cost, "source": SOURCE})
            # tubing leak (corrosion driven)
            p_leak = TUBING_LEAK_HAZARD * float(well["corrosion_index"])
            leaks = np.flatnonzero(rng.random(n_prod) < p_leak)
            for day in leaks[:1]:
                fid += 1
                wid_ += 1
                rig_h = float(rng.uniform(24, 72))
                down = rig_h + float(rng.uniform(6, 24))
                cost = rig_h * RIG_INR_PER_H + 35_000
                d = start + timedelta(days=int(a_p + day))
                fail.append({"failure_id": fid, "well_id": wid, "date": d, "cycle_no": cyc["cycle_no"],
                             "kind": "tubing_leak", "rod_index": None, "depth_m": float(rng.uniform(200, 1000)),
                             "mode": "tubing leak at collar", "goodman": None, "downtime_h": down,
                             "cost_inr": cost, "source": SOURCE})
                work.append({"workover_id": wid_, "well_id": wid, "date": d, "job_type": "tubing leak repair",
                             "trigger": "tubing_leak", "trigger_id": fid, "rig_hours": rig_h, "downtime_h": down,
                             "cost_inr": cost, "source": SOURCE})
            # pump unseating: daily hazard from viscous drag + pound impacts
            p = rows[rows.phase == "PRODUCTION"]
            fill = p["fillage"].to_numpy()
            v_up = np.pi * S_M * cyc["spm"] / 60
            uplift = pump_uplift_kn(p["viscosity_cp"].to_numpy(), v_up, fill)
            haz = pump_unseat_hazard(uplift, hold_down)
            for i in np.flatnonzero(rng.random(len(p)) < haz):
                uid += 1
                wid_ += 1
                rig_h = float(rng.uniform(8, 24))
                down = rig_h + float(rng.uniform(2, 12))
                cost = rig_h * RIG_INR_PER_H + 15_000
                row = p.iloc[i]
                d = row["date"]
                uns.append({"unseat_id": uid, "well_id": wid, "date": d, "cycle_no": cyc["cycle_no"],
                            "cycle_day": int(row["day"]), "uplift_kn": float(uplift[i]),
                            "hold_down_kn": hold_down, "viscosity_cp": float(row["viscosity_cp"]),
                            "downtime_h": down, "cost_inr": cost, "source": SOURCE})
                work.append({"workover_id": wid_, "well_id": wid, "date": d, "job_type": "pump reseat",
                             "trigger": "pump_unseat", "trigger_id": uid, "rig_hours": rig_h,
                             "downtime_h": down, "cost_inr": cost, "source": SOURCE})
            # scheduled maintenance every second cycle
            if cyc["cycle_no"] % 2 == 0 and cyc["complete"]:
                wid_ += 1
                rig_h = float(rng.uniform(6, 16))
                work.append({"workover_id": wid_, "well_id": wid,
                             "date": start + timedelta(days=int(cyc["n_days"]) + 2),
                             "job_type": str(rng.choice(["stuffing box repack", "gearbox oil change",
                                                         "belt/sheave change", "counterbalance adjustment"])),
                             "trigger": "scheduled", "trigger_id": None, "rig_hours": rig_h,
                             "downtime_h": rig_h, "cost_inr": rig_h * 4_000 + 9_000, "source": SOURCE})
    cols_f = ["failure_id", "well_id", "date", "cycle_no", "kind", "rod_index", "depth_m", "mode", "goodman",
              "downtime_h", "cost_inr", "source"]
    cols_u = ["unseat_id", "well_id", "date", "cycle_no", "cycle_day", "uplift_kn", "hold_down_kn",
              "viscosity_cp", "downtime_h", "cost_inr", "source"]
    cols_w = ["workover_id", "well_id", "date", "job_type", "trigger", "trigger_id", "rig_hours", "downtime_h",
              "cost_inr", "source"]
    return (pd.DataFrame(fail, columns=cols_f).astype({"rod_index": "Int64", "cycle_no": "Int64"}),
            pd.DataFrame(uns, columns=cols_u),
            pd.DataFrame(work, columns=cols_w).sort_values(["well_id", "date"]).reset_index(drop=True))
