from __future__ import annotations

import os


def main() -> None:
    import uvicorn

    uvicorn.run("mantle_api.main:app", host=os.environ.get("MANTLE_API_HOST", "127.0.0.1"),
                port=int(os.environ.get("MANTLE_API_PORT", "8000")), log_level="info")
