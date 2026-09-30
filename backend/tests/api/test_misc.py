from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pytest

API_SRC = Path(__file__).resolve().parents[2] / "packages" / "mantle-api" / "src" / "mantle_api"
BACKEND = Path(__file__).resolve().parents[2]


def test_no_module_imports_fixtures():
    bad = []
    for p in API_SRC.glob("*.py"):
        for n in ast.walk(ast.parse(p.read_text())):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or ""] if isinstance(n, ast.ImportFrom) else []
            if isinstance(n, ast.ImportFrom):
                names += [f"{n.module}.{a.name}" for a in n.names]
            if any("fixtures" in x for x in names):
                bad.append(p.name)
    assert not bad
    assert not (BACKEND / "packages/mantle-physics/src/mantle_physics/fixtures.py").exists()
    assert "fixtures" not in "".join(p.read_text() for p in API_SRC.glob("*.py")).replace("fixtures.py", "")


def test_api_process_never_imports_torch(api_db, tmp_path):
    code = ("import sys, lightgbm; from mantle_api.main import build_engine, warm; e = build_engine(); warm(e); "
            "print('torch' in sys.modules, flush=True)")
    import shutil

    db = tmp_path / "m.duckdb"
    shutil.copy(api_db, db)
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=BACKEND, timeout=180,
                       env={**os.environ, "MANTLE_API_DB": str(db)})
    assert r.stdout.strip().splitlines()[-1] == "False", r.stderr[-500:]


def test_openapi_export_is_up_to_date(client):
    p = BACKEND / "openapi.json"
    assert p.exists(), "run `uv run python -m mantle_api.export_openapi`"
    assert json.loads(p.read_text()) == client.app.openapi()


def test_latency_state_p95(client):
    """/state p95 < 150 ms once warm: repeated scenario queries (LRU) and first-time day scrubs on a warm well."""
    w = "/api/wells/BGW-17"
    client.get(f"{w}/state?day=41")
    hit = []
    for _ in range(60):
        t = time.perf_counter()
        client.get(f"{w}/state?day=41")
        hit.append(time.perf_counter() - t)
    assert np.percentile(hit, 95) < 0.15
    miss = []
    for d in range(20, 60):                                          # unseen days, same curve: twin + M4 + O1 + M5 recomputed
        t = time.perf_counter()
        assert client.get(f"{w}/state?day={d}.5").status_code == 200
        miss.append(time.perf_counter() - t)
    print("state p95 cold-day", np.percentile(miss, 95), "warm", np.percentile(hit, 95))
    assert np.percentile(miss, 95) < 0.6


@pytest.mark.slow
def test_startup_warm_time(client):
    assert client.app.state.warm_s < 60


def test_all_wells_serve_state(client):
    for wid in ("BGW-01", "BGW-30", "BGW-60"):
        r = client.get(f"/api/wells/{wid}/state")
        assert r.status_code == 200, wid
        assert client.get(f"/api/wells/{wid}/health").status_code == 200
