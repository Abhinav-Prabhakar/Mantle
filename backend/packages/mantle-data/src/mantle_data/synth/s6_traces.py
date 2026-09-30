"""S6: optimiser traces: random CSS-cycle decisions (state, action) -> outcome evaluated on the twin."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from mantle_physics.constants import PRICE, SOAK_END

from .common import SEED, SOURCE, Scale, get_scale, rng_for
from .wellmodel import cycle_run

CHUNK = 500
COLS = None  # filled lazily from the schema


def _chunk(args) -> pd.DataFrame:
    idx, n, seed, wells = args
    rng = rng_for(seed, "S6", idx)
    rows = []
    for j in range(n):
        w = wells[int(rng.integers(0, len(wells)))]
        cyc = int(rng.integers(1, 13))
        steam = float(rng.uniform(500, 1200))
        soak = float(rng.uniform(2, 10))
        cutoff = float(rng.uniform(40, 120))
        spm = float(rng.uniform(2, 9))
        kd = float(rng.uniform(0.4, 0.7))
        p_oil = PRICE["oil"] * float(rng.uniform(0.8, 1.2))
        p_steam = PRICE["steamT"] * float(rng.uniform(0.85, 1.15))
        oil_scale = w["pi_factor"] * w["decline_rate"] ** (cyc - 1)
        run = cycle_run(steam, spm, kd, steam_eff=w["steam_eff"], oil_scale=oil_scale,
                        visc_factor=w["visc_factor"], soak_days=soak)
        d1 = int(cutoff)
        sl = slice(SOAK_END, d1 + 1)
        oil = np.trapezoid(run.oil[sl])
        kwh = float(np.trapezoid(run.kw[sl]) * 24)
        net = float(np.trapezoid(run.oil[sl] * p_oil - run.kw[sl] * 24 * PRICE["kwh"]) - steam * p_steam)
        fill = run.fill[sl]
        pound = np.clip((0.85 - fill) / 0.35, 0, 1)
        rows.append({
            "trace_id": idx * CHUNK + j, "well_id": w["well_id"], "cycle_no": cyc,
            "state_pi_factor": w["pi_factor"], "state_visc_factor": w["visc_factor"],
            "state_steam_eff": w["steam_eff"], "state_decline": w["decline_rate"],
            "state_prev_cum_oil_bbl": float(3500 * oil_scale / w["decline_rate"]),
            "state_oil_price_inr": p_oil, "state_steam_cost_inr_per_t": p_steam,
            "action_steam_t": steam, "action_soak_d": soak, "action_cutoff_d": cutoff, "action_spm": spm,
            "action_kd": kd, "outcome_cum_oil_bbl": float(oil),
            "outcome_sor": float(steam * 6.2898 / oil) if oil > 5 else 99.0, "outcome_net_inr": net,
            "outcome_peak_sandface_t_c": float(run.T.max()),
            "outcome_min_float_margin": float(run.margin[sl].min()),
            "outcome_max_goodman": float(run.goodman[sl].max()),
            "outcome_mean_fillage": float(fill.mean()),
            "outcome_kwh_per_bbl": float(kwh / max(oil, 1.0)),
            "outcome_impacts_per_day": float((spm * 1440 * pound).mean()), "source": SOURCE,
        })
    return pd.DataFrame(rows)


def generate(wells: pd.DataFrame, scale: str | Scale = "default", seed: int = SEED, workers: int | None = None
             ) -> pd.DataFrame:
    sc = get_scale(scale)
    wl = wells[["well_id", "pi_factor", "visc_factor", "steam_eff", "decline_rate"]].to_dict("records")
    jobs = [(i, min(CHUNK, sc.n_traces - i * CHUNK), seed, wl) for i in range((sc.n_traces + CHUNK - 1) // CHUNK)]
    workers = workers if workers is not None else (min(os.cpu_count() or 1, 8) if sc.n_traces > 4000 else 1)
    if workers > 1:
        with ProcessPoolExecutor(workers) as ex:
            parts = list(ex.map(_chunk, jobs))
    else:
        parts = [_chunk(j) for j in jobs]
    return pd.concat(parts, ignore_index=True)
