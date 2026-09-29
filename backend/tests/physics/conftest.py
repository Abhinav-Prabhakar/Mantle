from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).parent


@pytest.fixture(scope="session")
def oracle(tmp_path_factory):
    """Run the JS twin under Node once and return its dump (skips if node is unavailable)."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node not installed; JS parity tests skipped")
    out = tmp_path_factory.mktemp("oracle") / "oracle.json"
    r = subprocess.run([node, str(HERE / "js_oracle.mjs"), str(out)], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        pytest.skip(f"node oracle failed to run: {r.stderr[:300]}")
    return json.loads(out.read_text())
