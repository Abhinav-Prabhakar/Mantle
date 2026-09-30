"""R4: Volve production data loader (Equinor Open Data Licence; manual download, never fetched)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..paths import processed_dir, raw_dir
from .common import update_licenses

LICENCE = (
    "Equinor Volve Data Village, Equinor Open Data Licence (research/education; click-through, manual "
    "download from https://www.equinor.com/energy/volve-data-sharing). Not redistributed by this repo."
)
FILE = "volve_production.xlsx"


def load_volve(path: Path | None = None) -> Path | None:
    """Normalise a user-supplied Volve production workbook; returns None (with a message) if absent."""
    path = path or raw_dir() / FILE
    if not path.exists():
        print(f"[volve] {path} not found: skipping. Download 'Volve production data' manually "
              "(Equinor Open Data Licence) and save it there to enable this optional dataset.")
        return None
    sheets = pd.read_excel(path, sheet_name=None)
    frames = [df for df in sheets.values() if len(df) and any("date" in str(c).lower() for c in df.columns)]
    if not frames:
        raise ValueError(f"no production sheet with a date column in {path}")
    df = max(frames, key=len).copy()
    df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    datecol = next(c for c in df.columns if "date" in c)
    df = df.rename(columns={datecol: "date"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["source"] = "real"
    out = processed_dir() / "volve_production.parquet"
    df.to_parquet(out, index=False)
    update_licenses(raw_dir(), "R4 Volve", LICENCE)
    return out
