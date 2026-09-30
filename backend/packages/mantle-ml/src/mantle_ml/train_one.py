"""Subprocess entry: ``python -m mantle_ml.train_one M3 [--quick] [--root DIR]`` trains one model in a clean process."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import common
from .train import MODULES, _mod, update_registry


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", choices=list(MODULES))
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--root", default=None)
    a = ap.parse_args()
    root = Path(a.root) if a.root else common.models_dir()
    ev = _mod(a.model).train(root, quick=a.quick)
    ev.setdefault("trained_at", common.now_iso())
    (root / a.model / "eval.json").write_text(json.dumps(ev, indent=2))
    update_registry(root, a.model, ev)
    p = ev.get("primary", {})
    print(f"[{a.model}] done in {ev.get('train_seconds')} s  primary={p.get('name')}={p.get('value')}", flush=True)


if __name__ == "__main__":
    main()
