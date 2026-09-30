"""Train orchestration: run models by id, write artifacts and update ``models/registry.json``."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from . import common

MODULES: dict[str, str] = {
    "M0": "m0_viscosity", "M1": "m1_thermal", "M2": "m2_forecast", "M3": "m3_dyno", "M5": "m5_stroke",
    "M4": "m4_risk", "M6": "m6_anomaly", "O1": "o1_srp", "O2": "o2_css", "O3": "o3_rl",
}
ORDER = list(MODULES)


def _mod(mid: str):
    return importlib.import_module(f"mantle_ml.models.{MODULES[mid]}")


def available() -> list[str]:
    out = []
    for m in ORDER:
        try:
            importlib.import_module(f"mantle_ml.models.{MODULES[m]}")
            out.append(m)
        except ModuleNotFoundError as e:
            if not str(e).endswith(f"{MODULES[m]}'"):
                raise
    return out


def update_registry(root: Path, mid: str, ev: dict) -> None:
    p = root / "registry.json"
    reg = json.loads(p.read_text()) if p.exists() else {"models": {}}
    prim = ev.get("primary", {})
    reg["models"][mid] = {
        "id": mid, "version": ev.get("version", "1.0.0"), "trained_at": ev.get("trained_at", common.now_iso()),
        "data_hash": ev.get("data_hash", ""), "source": ev.get("source", "physics_synthetic"),
        "metrics": {"primary": prim, **{k: v for k, v in ev.get("metrics", {}).items() if isinstance(v, (int, float))}},
        "train_seconds": ev.get("train_seconds"), "size_bytes": common.dir_size_bytes(root / mid),
        "quick": ev.get("quick", False),
    }
    p.write_text(json.dumps(reg, indent=2, sort_keys=True))


def train(ids: list[str] | None = None, quick: bool = False, root: Path | None = None, log=print,
          in_process: bool = False) -> dict[str, dict]:
    """Train models. Each one runs in its own subprocess (see the OpenMP note in ``mantle_ml/__init__``)."""
    import os
    import subprocess
    import sys

    root = Path(root) if root else common.models_dir()
    ids = ids or available()
    out: dict[str, dict] = {}
    for mid in ids:
        log(f"[{mid}] training{' (quick)' if quick else ''} ...")
        if in_process:
            ev = _mod(mid).train(root, quick=quick)
            ev.setdefault("trained_at", common.now_iso())
            (root / mid / "eval.json").write_text(json.dumps(ev, indent=2))
            update_registry(root, mid, ev)
        else:
            env = dict(os.environ, MANTLE_TORCH_THREADS="8" if mid == "M3" else "1")
            cmd = [sys.executable, "-m", "mantle_ml.train_one", mid, "--root", str(root)] + (["--quick"] if quick else [])
            r = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"training {mid} failed ({r.returncode}):\n{r.stdout[-1500:]}\n{r.stderr[-3000:]}")
            log(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else f"[{mid}] done")
            ev = json.loads((root / mid / "eval.json").read_text())
        out[mid] = ev
    return out
