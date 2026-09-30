"""S4: dynamometer cards. 12 balanced classes from ``mantle_physics.dyno.synthesize_cards`` + augmentations."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from mantle_physics import DYNO_CLASSES, synthesize_cards

from .common import SEED, SOURCE, Scale, get_scale, rng_for

N_PTS = 128
AUGMENTATIONS = ("none", "noise", "drift", "clipped", "missing", "shift", "combo")
AUG_P = np.array([0.35, 0.18, 0.12, 0.10, 0.10, 0.08, 0.07])
BATCH = 20_000
SHARD = 50_000
ARRAY_COLS = ("surface_pos", "surface_load", "downhole_pos", "downhole_load")


def balanced_labels(n: int, rng: np.random.Generator) -> np.ndarray:
    k = len(DYNO_CLASSES)
    lab = np.arange(n) % k
    return rng.permutation(lab)


def augment(pos: np.ndarray, load: np.ndarray, aug: np.ndarray, rng: np.random.Generator
            ) -> tuple[np.ndarray, np.ndarray]:
    """Apply per-row augmentations (``aug`` holds indices into AUGMENTATIONS); returns copies."""
    pos, load = pos.copy(), load.copy()
    n = pos.shape[1]
    ptp = np.ptp(load, axis=1)
    sp = np.ptp(pos, axis=1)
    B = len(pos)
    noisy = np.isin(aug, [1, 6])
    if noisy.any():
        load[noisy] += rng.standard_normal((noisy.sum(), n)) * (0.015 * ptp[noisy])[:, None]
        pos[noisy] += rng.standard_normal((noisy.sum(), n)) * (0.003 * sp[noisy])[:, None]
    drift = np.isin(aug, [2, 6])
    if drift.any():
        k = drift.sum()
        gain = rng.uniform(0.97, 1.03, k)[:, None]
        off = rng.uniform(-0.03, 0.03, k)[:, None] * ptp[drift][:, None]
        ramp = rng.uniform(-0.03, 0.03, k)[:, None] * ptp[drift][:, None] * np.linspace(0, 1, n)[None]
        load[drift] = load[drift] * gain + off + ramp
    clip = aug == 3
    if clip.any():
        lo = load[clip].min(axis=1, keepdims=True)
        cap = lo + rng.uniform(0.7, 0.9, (clip.sum(), 1)) * ptp[clip][:, None]
        load[clip] = np.minimum(load[clip], cap)
    miss = np.flatnonzero(aug == 4)
    for i in miss:
        w = int(rng.uniform(0.05, 0.15) * n)
        s = int(rng.integers(1, n - w - 1))
        for arr in (pos, load):
            arr[i, s: s + w] = np.linspace(arr[i, s - 1], arr[i, s + w], w + 2)[1:-1]
    shift = np.flatnonzero(np.isin(aug, [5, 6]))
    for i in shift:
        r = int(rng.integers(0, n))
        pos[i], load[i] = np.roll(pos[i], r), np.roll(load[i], r)
    return pos, load


def generate_batches(scale: str | Scale = "default", seed: int = SEED, well_ids: list[str] | None = None,
                     batch: int = BATCH) -> Iterator[pd.DataFrame]:
    sc = get_scale(scale)
    rng = rng_for(seed, "S4")
    labels_all = balanced_labels(sc.n_cards, rng)
    ids = np.array(well_ids or [f"BGW-{i:02d}" for i in range(1, sc.n_wells + 1)])
    done = 0
    for b0 in range(0, sc.n_cards, batch):
        labels = labels_all[b0: b0 + batch]
        cards = synthesize_cards(labels, rng, n_points=N_PTS)
        aug = rng.choice(len(AUGMENTATIONS), size=len(labels), p=AUG_P)
        sp, sl = augment(cards.surface_pos, cards.surface_load, aug, rng)
        p = cards.params
        df = pd.DataFrame({
            "card_id": np.arange(done, done + len(labels)),
            "well_id": rng.choice(ids, len(labels)),
            "label": [DYNO_CLASSES[i] for i in labels],
            "label_idx": labels.astype(np.int64),
            "spm": p["spm"], "stroke_m": p["stroke"], "kd": p["kd"], "fillage": p["fillage"],
            "damping": p["damping"],
            "augmentation": [AUGMENTATIONS[i] for i in aug],
            "source": SOURCE,
        })
        for name, arr in zip(ARRAY_COLS, (sp, sl, cards.dh_pos, cards.dh_load), strict=True):
            df[name] = list(arr.astype(np.float32))
        done += len(labels)
        yield df


def generate(scale: str | Scale = "default", seed: int = SEED, **kw) -> pd.DataFrame:
    return pd.concat(list(generate_batches(scale, seed, **kw)), ignore_index=True)


def _to_table(df: pd.DataFrame) -> pa.Table:
    cols = {}
    for c in df.columns:
        if c in ARRAY_COLS:
            flat = np.concatenate(df[c].to_numpy()).astype(np.float32)
            cols[c] = pa.FixedSizeListArray.from_arrays(pa.array(flat), N_PTS)
        else:
            cols[c] = pa.array(df[c].to_numpy() if df[c].dtype != object else df[c].tolist())
    return pa.table(cols)


def write(out_dir: Path, scale: str | Scale = "default", seed: int = SEED, well_ids=None) -> int:
    """Stream batches into ``out_dir/dyno_cards/part-NNN.parquet`` shards; returns the number of cards."""
    d = out_dir / "dyno_cards"
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("part-*.parquet"):
        old.unlink()
    n, shard, buf = 0, 0, []
    rows = 0
    for df in generate_batches(scale, seed, well_ids):
        buf.append(df)
        rows += len(df)
        n += len(df)
        if rows >= SHARD:
            pq.write_table(_to_table(pd.concat(buf, ignore_index=True)), d / f"part-{shard:03d}.parquet",
                           compression="zstd")
            shard, buf, rows = shard + 1, [], 0
    if buf:
        pq.write_table(_to_table(pd.concat(buf, ignore_index=True)), d / f"part-{shard:03d}.parquet",
                       compression="zstd")
    return n
