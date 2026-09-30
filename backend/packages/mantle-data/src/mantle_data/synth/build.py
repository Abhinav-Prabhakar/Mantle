"""Orchestrate the physics-synthetic build (S1-S6) into ``data/synthetic`` and load DuckDB."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from ..paths import synthetic_dir
from . import s1_roster, s2_cycles, s3_telemetry, s4_cards, s5_failures, s6_traces
from .common import SEED, Scale, frame_hash, get_scale, write_parquet

STAGES = ("S1", "S2", "S3", "S4", "S5", "S6")


def parse_only(only: str | list[str] | None) -> list[str]:
    if not only:
        return list(STAGES)
    items = only.split(",") if isinstance(only, str) else only
    items = [i.strip().upper() for i in items if i.strip()]
    bad = [i for i in items if i not in STAGES]
    if bad:
        raise ValueError(f"unknown stage(s) {bad}; choose from {STAGES}")
    return items


def build(scale: str | Scale = "default", only=None, seed: int = SEED, out_dir: Path | None = None,
          load_db: bool = True, log=print) -> dict:
    sc = get_scale(scale)
    out = Path(out_dir) if out_dir else synthetic_dir()
    out.mkdir(parents=True, exist_ok=True)
    stages = parse_only(only)
    info: dict = {"scale": sc.name, "seed": seed, "stages": {}}
    cache: dict[str, pd.DataFrame] = {}

    def timed(name, fn):
        t = time.time()
        r = fn()
        info["stages"][name] = {"seconds": round(time.time() - t, 2)}
        log(f"[{name}] {info['stages'][name]['seconds']} s")
        return r

    def wells() -> pd.DataFrame:
        if "wells" not in cache:
            cache["wells"] = s1_roster.generate(sc, seed)
        return cache["wells"]

    def cycles() -> tuple[pd.DataFrame, pd.DataFrame]:
        if "cycles" not in cache:
            cache["cycles"], cache["daily"] = s2_cycles.generate(wells(), sc, seed)
        return cache["cycles"], cache["daily"]

    if "S1" in stages:
        df = timed("S1", wells)
        write_parquet(df, out / "wells.parquet")
        info["stages"]["S1"].update(rows=len(df), hash=frame_hash(df))
    if "S2" in stages:
        c, d = timed("S2", cycles)
        write_parquet(c, out / "cycles.parquet")
        write_parquet(d, out / "cycle_daily.parquet")
        info["stages"]["S2"].update(rows=len(c), daily_rows=len(d), hash=frame_hash(c))
    if "S3" in stages:
        c, _ = cycles()
        ev = timed("S3", lambda: s3_telemetry.generate(wells(), c, sc, seed, out))
        write_parquet(ev, out / "telemetry_events.parquet")
        n = sum(pd.read_parquet(p, columns=["ts"]).shape[0] for p in (out / "telemetry").glob("*/*.parquet"))
        info["stages"]["S3"].update(rows=n, events=len(ev))
    if "S4" in stages:
        n = timed("S4", lambda: s4_cards.write(out, sc, seed, list(wells()["well_id"])))
        info["stages"]["S4"].update(rows=n)
    if "S5" in stages:
        c, d = cycles()
        f, u, w = timed("S5", lambda: s5_failures.generate(wells(), c, d, seed))
        write_parquet(f, out / "failures.parquet")
        write_parquet(u, out / "unseats.parquet")
        write_parquet(w, out / "workovers.parquet")
        info["stages"]["S5"].update(failures=len(f), unseats=len(u), workovers=len(w), hash=frame_hash(f))
    if "S6" in stages:
        t = timed("S6", lambda: s6_traces.generate(wells(), sc, seed))
        write_parquet(t, out / "optimiser_traces.parquet")
        info["stages"]["S6"].update(rows=len(t), hash=frame_hash(t))
    info["bytes"] = {str(p.relative_to(out)): p.stat().st_size for p in out.rglob("*.parquet")}
    (out / "manifest.json").write_text(json.dumps(info, indent=2, default=str))
    if load_db:
        from .. import db

        t = time.time()
        db.load(synthetic=out)
        log(f"[db] loaded in {time.time() - t:.1f} s")
    return info
