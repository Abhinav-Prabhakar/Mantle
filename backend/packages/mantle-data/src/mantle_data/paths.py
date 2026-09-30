"""Data directory layout. Override the root with ``MANTLE_DATA_DIR`` (tests do)."""

from __future__ import annotations

import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[4]


def data_dir() -> Path:
    return Path(os.environ.get("MANTLE_DATA_DIR", BACKEND_DIR / "data"))


def raw_dir() -> Path:
    return _mk(data_dir() / "raw")


def processed_dir() -> Path:
    return _mk(data_dir() / "processed")


def synthetic_dir() -> Path:
    return _mk(data_dir() / "synthetic")


def llm_dir() -> Path:
    return _mk(data_dir() / "llm")


def reference_dir() -> Path:
    return _mk(data_dir() / "reference")


def db_path() -> Path:
    return data_dir() / "mantle.duckdb"


def prompts_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "prompts"


def _mk(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p
