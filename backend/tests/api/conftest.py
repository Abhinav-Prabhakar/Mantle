from __future__ import annotations

import re
import shutil

import pytest
from fastapi.testclient import TestClient

from mantle_data import paths


def _camel(o):
    """The frontend client's snake_case -> camelCase (app/js/api.js ``camel``), recursively."""
    if isinstance(o, list):
        return [_camel(v) for v in o]
    if isinstance(o, dict):
        return {re.sub(r"_([a-z0-9])", lambda m: m.group(1).upper(), k): _camel(v) for k, v in o.items()}
    return o


@pytest.fixture(scope="session")
def api_db(tmp_path_factory):
    src = paths.db_path()
    if not src.exists():
        pytest.skip("no data/mantle.duckdb (run `uv run mantle-data build --only S1,S2,S5`)")
    dst = tmp_path_factory.mktemp("apidb") / "mantle.duckdb"
    shutil.copy(src, dst)
    return dst


@pytest.fixture(scope="session")
def client(api_db):
    mp = pytest.MonkeyPatch()
    mp.setenv("MANTLE_API_DB", str(api_db))
    from mantle_api.main import app

    with TestClient(app) as c:
        yield c
    mp.undo()


@pytest.fixture(scope="session")
def engine(client):
    return client.app.state.engine


@pytest.fixture(scope="session")
def camel():
    return _camel
