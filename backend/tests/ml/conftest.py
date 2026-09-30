from __future__ import annotations

import json
from pathlib import Path

import pytest

from mantle_data import paths

REAL_MODELS = paths.BACKEND_DIR / "models"


@pytest.fixture(scope="session")
def ml_data(tmp_path_factory):
    """Small-scale synthetic data in an isolated data dir (3W sample symlinked from the real data if present)."""
    root = tmp_path_factory.mktemp("ml_data")
    real_3w = paths.BACKEND_DIR / "data" / "processed" / "threew_sample.parquet"
    mp = pytest.MonkeyPatch()
    mp.setenv("MANTLE_DATA_DIR", str(root))
    (root / "processed").mkdir()
    if real_3w.exists():
        (root / "processed" / "threew_sample.parquet").symlink_to(real_3w)
    from mantle_ml import data

    data.ensure_small_data()
    yield root
    mp.undo()


@pytest.fixture(scope="session")
def quick_models(tmp_path_factory):
    """Directory into which quick-mode trainings are written (shared across tests)."""
    return tmp_path_factory.mktemp("quick_models")


def real_eval(mid: str) -> dict:
    p = REAL_MODELS / mid / "eval.json"
    if not p.exists():
        pytest.skip(f"no shipped artifact for {mid}")
    return json.loads(Path(p).read_text())


@pytest.fixture
def shipped():
    return real_eval
