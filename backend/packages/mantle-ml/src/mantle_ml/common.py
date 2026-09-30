"""Shared helpers: artifact directories, eval/card writing, timing, data hashing, seeds."""

from __future__ import annotations

import hashlib
import json
import os
import time
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

SEED = 20260930


def backend_dir() -> Path:
    from mantle_data.paths import BACKEND_DIR

    return Path(BACKEND_DIR)


def models_dir() -> Path:
    """Where artifacts live. Override with ``MANTLE_MODELS_DIR`` (tests do)."""
    p = Path(os.environ.get("MANTLE_MODELS_DIR", backend_dir() / "models"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def model_dir(model_id: str, root: Path | None = None) -> Path:
    p = (Path(root) if root else models_dir()) / model_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@contextmanager
def timer():
    t = {"seconds": 0.0}
    t0 = time.perf_counter()
    try:
        yield t
    finally:
        t["seconds"] = round(time.perf_counter() - t0, 2)


def data_hash(items: Iterable[Any]) -> str:
    """Short content hash of DataFrames / arrays / files / strings (used as ``data_hash`` in the registry)."""
    import pandas as pd

    h = hashlib.sha256()
    for it in items:
        if isinstance(it, pd.DataFrame):
            h.update(str(list(it.columns)).encode())
            h.update(str(it.shape).encode())
            num = it.select_dtypes("number")
            if len(num):
                h.update(np.ascontiguousarray(num.to_numpy(dtype=float)[:: max(1, len(num) // 2000)]).tobytes())
        elif isinstance(it, np.ndarray):
            h.update(str(it.shape).encode())
            h.update(np.ascontiguousarray(it.ravel()[:: max(1, it.size // 5000)]).tobytes())
        elif isinstance(it, Path):
            st = it.stat()
            h.update(f"{it.name}:{st.st_size}".encode())
        else:
            h.update(str(it).encode())
    return h.hexdigest()[:16]


def _clean(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return None if f != f or f in (float("inf"), float("-inf")) else round(f, 6)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    return o


def write_eval(out_dir: Path, model_id: str, ev: dict, card: str) -> dict:
    """Write ``eval.json`` and ``card.md`` into ``out_dir`` and return the cleaned eval dict."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ev = _clean({"model": model_id, **ev})
    (out_dir / "eval.json").write_text(json.dumps(ev, indent=2, sort_keys=False))
    (out_dir / "card.md").write_text(card.strip() + "\n")
    return ev


def read_eval(out_dir: Path) -> dict:
    return json.loads((Path(out_dir) / "eval.json").read_text())


def dir_size_bytes(p: Path) -> int:
    return sum(f.stat().st_size for f in Path(p).rglob("*") if f.is_file())


def rng(seed: int = SEED, *extra: int) -> np.random.Generator:
    return np.random.default_rng([seed, *extra])
