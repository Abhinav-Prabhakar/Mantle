"""Data access for training/eval. Reads parquet lazily; never copies the big tables to disk."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from mantle_data.paths import processed_dir, synthetic_dir

SOURCE_PHYS = "physics_synthetic"


def _read(name: str, cols: list[str] | None = None) -> pd.DataFrame:
    p = synthetic_dir() / f"{name}.parquet"
    if not p.exists():
        raise FileNotFoundError(f"{p} missing: run `uv run mantle-data build` first")
    return pd.read_parquet(p, columns=cols)


def wells() -> pd.DataFrame:
    return _read("wells")


def cycles() -> pd.DataFrame:
    return _read("cycles")


def cycle_daily() -> pd.DataFrame:
    return _read("cycle_daily")


def failures() -> pd.DataFrame:
    return _read("failures")


def unseats() -> pd.DataFrame:
    return _read("unseats")


def workovers() -> pd.DataFrame:
    return _read("workovers")


def traces() -> pd.DataFrame:
    return _read("optimiser_traces")


def events() -> pd.DataFrame:
    return _read("telemetry_events")


def card_files() -> list[Path]:
    return sorted((synthetic_dir() / "dyno_cards").glob("part-*.parquet"))


def read_cards(n: int, seed: int = 0, offset_frac: float = 0.0) -> dict[str, np.ndarray]:
    """Read ``n`` cards spread over all shards (row-group sampling; the file is never loaded whole).

    Returns arrays ``surface_pos, surface_load`` (n,128), ``label_idx``, ``spm``, ``stroke_m``, ``kd``,
    ``fillage``, ``damping``, ``card_id``.
    """
    files = card_files()
    if not files:
        raise FileNotFoundError("no dyno_cards: run `uv run mantle-data build`")
    rng = np.random.default_rng(seed)
    groups = [(f, g) for f in files for g in range(pq.ParquetFile(f).num_row_groups)]
    order = rng.permutation(len(groups))
    cols = ["card_id", "label_idx", "spm", "stroke_m", "kd", "fillage", "damping", "surface_pos", "surface_load"]
    parts: list[pd.DataFrame] = []
    got = 0
    for gi in order:
        f, g = groups[gi]
        t = pq.ParquetFile(f).read_row_group(g, columns=cols)
        df = t.to_pandas()
        parts.append(df)
        got += len(df)
        if got >= n * 1.3:
            break
    df = pd.concat(parts, ignore_index=True)
    df = df.iloc[rng.permutation(len(df))[:n]]
    out = {c: df[c].to_numpy() for c in ("card_id", "label_idx", "spm", "stroke_m", "kd", "fillage", "damping")}
    out["surface_pos"] = np.stack(df["surface_pos"].to_numpy()).astype(np.float32)
    out["surface_load"] = np.stack(df["surface_load"].to_numpy()).astype(np.float32)
    return out


def threew_sample_path() -> Path:
    return processed_dir() / "threew_sample.parquet"


def telemetry_wells() -> list[str]:
    root = synthetic_dir() / "telemetry"
    return sorted(p.name.split("=", 1)[1] for p in root.glob("well_id=*"))


def telemetry_path(well_id: str) -> Path:
    return synthetic_dir() / "telemetry" / f"well_id={well_id}" / "part-0.parquet"


def data_files_fingerprint() -> list[Path]:
    return [p for p in [synthetic_dir() / f"{n}.parquet" for n in ("wells", "cycles", "cycle_daily")] if p.exists()]


def ensure_small_data() -> None:
    """Make sure the synthetic tables exist, building a *small* set into the active data dir if they don't."""
    if (synthetic_dir() / "cycle_daily.parquet").exists() and card_files():
        return
    from mantle_data.synth.build import build

    build("small", out_dir=synthetic_dir(), load_db=False, log=lambda *_: None)
