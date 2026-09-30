from __future__ import annotations

import os
import shutil
from pathlib import Path


def seed_db() -> None:
    """Container start: copy the image's baked database into the data volume the first time (audit log persists there)."""
    seed = os.environ.get("MANTLE_DB_SEED")
    if not seed or not Path(seed).exists():
        return
    from .settings import get_settings

    dst = get_settings().db_path
    if not dst.exists() and dst.resolve() != Path(seed).resolve():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(seed, dst)


def main() -> None:
    import uvicorn

    seed_db()
    uvicorn.run("mantle_api.main:app", host=os.environ.get("MANTLE_API_HOST", "127.0.0.1"),
                port=int(os.environ.get("MANTLE_API_PORT", "8000")), log_level="info")
