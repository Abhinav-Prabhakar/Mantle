from __future__ import annotations

import contextlib
import os

import pytest


def pytest_addoption(parser):
    with contextlib.suppress(ValueError):      # may already be registered
        parser.addoption("--runslow", action="store_true", default=False, help="run @pytest.mark.slow tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow") or os.environ.get("MANTLE_RUN_SLOW"):
        return
    skip = pytest.mark.skip(reason="slow test (use --runslow)")
    for it in items:
        if "slow" in it.keywords:
            it.add_marker(skip)
