from __future__ import annotations

import contextlib
import os

import pytest

from mantle_data import db
from mantle_data.synth.build import build


def pytest_addoption(parser):
    with contextlib.suppress(ValueError):      # may already be registered by another conftest
        parser.addoption("--run-network", action="store_true", default=False, help="run @network tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "network: hits the real network (skipped unless --run-network)")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-network") or os.environ.get("MANTLE_RUN_NETWORK"):
        return
    skip = pytest.mark.skip(reason="network test (use --run-network)")
    for it in items:
        if "network" in it.keywords:
            it.add_marker(skip)


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    """One small-scale build (S1-S6 + DuckDB) shared by the data tests, in an isolated data dir."""
    root = tmp_path_factory.mktemp("mantle_data")
    mp = pytest.MonkeyPatch()
    mp.setenv("MANTLE_DATA_DIR", str(root))
    info = build("small", out_dir=root / "synthetic", log=lambda *_: None)
    yield {"root": root, "syn": root / "synthetic", "info": info, "db": db.db_path()}
    mp.undo()
