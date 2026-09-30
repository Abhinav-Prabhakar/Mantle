"""R2: Open-Meteo historical weather for Baghewala (CC BY 4.0)."""

from __future__ import annotations

import time
from datetime import date, timedelta
from pathlib import Path

import httpx
import pandas as pd

from ..paths import processed_dir, raw_dir
from .common import sha256_bytes, update_licenses, write_manifest

URL = "https://archive-api.open-meteo.com/v1/archive"
LAT, LON = 27.95, 71.95
START = date(2018, 1, 1)
VARS = ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "shortwave_radiation"]
LICENCE = (
    "Open-Meteo historical weather API, CC BY 4.0 (https://open-meteo.com/en/license). Weather data by "
    "Open-Meteo.com, based on ERA5 / ERA5-Land (Copernicus Climate Change Service, Hersbach et al. 2020). "
    f"Location {LAT} N, {LON} E (Baghewala, Rajasthan), timezone Asia/Kolkata."
)


def _get(client: httpx.Client, params: dict, retries: int = 8) -> bytes:
    for i in range(retries):
        try:
            r = client.get(URL, params=params)
            if r.status_code == 429:
                time.sleep(min(60, 5 * 2**i))
                continue
            r.raise_for_status()
            return r.content
        except httpx.HTTPError:
            if i == retries - 1:
                raise
            time.sleep(min(60, 2 * 2**i))
    raise RuntimeError("unreachable")


def fetch_weather(end: date | None = None, client: httpx.Client | None = None, force: bool = False) -> Path:
    """Fetch (yearly chunks, cached as raw JSON) and normalise to ``processed/weather.parquet``."""
    end = end or (date.today() - timedelta(days=1))
    raw = raw_dir() / "open_meteo"
    raw.mkdir(exist_ok=True)
    own = client is None
    client = client or httpx.Client(timeout=60.0)
    frames, manifest = [], {}
    try:
        for year in range(START.year, end.year + 1):
            a, b = max(START, date(year, 1, 1)), min(end, date(year, 12, 31))
            cache = raw / f"{year}_{b.isoformat()}.json"
            if force or not cache.exists():
                for old in raw.glob(f"{year}_*.json"):
                    old.unlink()
                data = _get(client, {
                    "latitude": LAT, "longitude": LON, "start_date": a.isoformat(), "end_date": b.isoformat(),
                    "hourly": ",".join(VARS), "timezone": "Asia/Kolkata",
                })
                cache.write_bytes(data)
            data = cache.read_bytes()
            manifest[cache.name] = sha256_bytes(data)
            frames.append(_normalise(data))
    finally:
        if own:
            client.close()
    df = pd.concat(frames, ignore_index=True).drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    out = processed_dir() / "weather.parquet"
    df.to_parquet(out, index=False, compression="zstd")
    write_manifest(raw / "manifest.json", manifest)
    update_licenses(raw_dir(), "R2 Open-Meteo weather", LICENCE)
    return out


def _normalise(payload: bytes) -> pd.DataFrame:
    import json

    j = json.loads(payload)
    h = j["hourly"]
    df = pd.DataFrame({"ts": pd.to_datetime(h["time"])})
    df["temperature_c"] = h["temperature_2m"]
    df["relative_humidity_pct"] = h["relative_humidity_2m"]
    df["wind_speed_kmh"] = h["wind_speed_10m"]
    df["shortwave_wm2"] = h["shortwave_radiation"]
    df["source"] = "real"
    return df
