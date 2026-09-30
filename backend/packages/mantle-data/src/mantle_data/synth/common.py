"""Scales, seeding, hashing and parquet helpers shared by the physics-synthetic generators."""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260930
SOURCE = "physics_synthetic"
SHOWCASE_ID = "BGW-17"


@dataclass(frozen=True)
class Scale:
    name: str
    n_wells: int              # S1 roster
    cycle_wells: int          # wells with S2 histories
    cycles: tuple[int, int]   # completed cycles per well (min, max), before the in-progress one
    tele_wells: int
    tele_days: int
    tele_hz: float
    n_cards: int
    n_traces: int


SCALES: dict[str, Scale] = {
    "small": Scale("small", 20, 4, (2, 3), 2, 1, 1.0, 1_200, 400),
    "default": Scale("default", 60, 60, (6, 12), 20, 30, 1.0, 200_000, 50_000),
    "enormous": Scale("enormous", 400, 400, (10, 15), 200, 180, 1.0, 2_000_000, 500_000),
}


def get_scale(name: str | Scale) -> Scale:
    if isinstance(name, Scale):
        return name
    if name not in SCALES:
        raise ValueError(f"unknown scale {name!r}; choose from {sorted(SCALES)}")
    return SCALES[name]


def rng_for(seed: int, stage: str, *extra: int) -> np.random.Generator:
    return np.random.default_rng([seed, zlib.crc32(stage.encode()), *extra])


def frame_hash(df: pd.DataFrame) -> str:
    """Order-sensitive content hash of a DataFrame (arrays/objects hashed via their string form)."""
    import hashlib

    h = hashlib.sha256()
    for c in df.columns:
        s = df[c]
        if s.dtype == object:
            s = s.map(lambda v: v.tobytes().hex() if hasattr(v, "tobytes") else str(v))
        h.update(str(c).encode())
        h.update(pd.util.hash_pandas_object(s, index=False).values.tobytes())
    return h.hexdigest()


def write_parquet(df: pd.DataFrame, path: Path, **kw) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, compression="zstd", **kw)
    return path
