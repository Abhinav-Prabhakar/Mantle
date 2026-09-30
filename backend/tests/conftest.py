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


_EXIT = {"code": None}


def pytest_sessionfinish(session, exitstatus):
    _EXIT["code"] = int(exitstatus)


def pytest_unconfigure(config):
    """torch + lightgbm each ship a libomp; their destructors abort at interpreter teardown on macOS.
    Exit hard (after the summary is printed) once both have been loaded so the process status stays truthful."""
    import sys

    if _EXIT["code"] is not None and "torch" in sys.modules and "lightgbm" in sys.modules:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(_EXIT["code"])
