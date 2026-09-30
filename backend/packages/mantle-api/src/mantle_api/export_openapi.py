"""Write backend/openapi.json (``uv run python -m mantle_api.export_openapi``)."""

from __future__ import annotations

import json
from pathlib import Path

from .main import create_app


def main() -> None:
    p = Path(__file__).resolve().parents[4] / "openapi.json"
    p.write_text(json.dumps(create_app().openapi(), indent=2, sort_keys=False) + "\n")
    print(f"wrote {p}")


if __name__ == "__main__":
    main()
