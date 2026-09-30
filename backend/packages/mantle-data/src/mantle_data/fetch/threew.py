"""R1: Petrobras 3W v2.0.0 (CC BY 4.0) -- download, convert to parquet, compact sample."""

from __future__ import annotations

import io
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from ..paths import processed_dir, raw_dir
from .common import Progress, download, read_manifest, sha256_file, update_licenses, write_manifest

URL = "https://ndownloader.figshare.com/files/55019255"
ZIP_NAME = "3w_dataset_2.0.0.zip"
LICENCE = (
    "Petrobras 3W Dataset v2.0.0, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). "
    "Source: https://figshare.com/ (file 55019255). Citation: Vargas, R. E. V., Munaro, C. J., Ciarelli, P. M., "
    "Medeiros, A. G., Amaral, B. G., Barrionuevo, D. C., de Araujo, J. C. D., Ribeiro, J. L., Magalhaes, L. P. "
    "(2019). A realistic and public dataset with rare undesirable real events in oil wells. Journal of Petroleum "
    "Science and Engineering, 181, 106223; and the 3W Project (github.com/petrobras/3W)."
)
EVENT_NAMES = {
    0: "normal", 1: "abrupt_bsw_increase", 2: "spurious_dhsv_closure", 3: "severe_slugging",
    4: "flow_instability", 5: "rapid_productivity_loss", 6: "quick_pck_restriction",
    7: "pck_scaling", 8: "production_line_hydrate", 9: "service_line_hydrate",
}
_INST = re.compile(r"(?P<origin>WELL|SIMULATED|DRAWN)-(?P<num>\d+)_(?P<ts>\d{14})", re.I)


def remote_size(url: str = URL, client: httpx.Client | None = None) -> int | None:
    own = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=30.0)
    try:
        r = client.get(url, headers={"Range": "bytes=0-0"})
        cr = r.headers.get("content-range", "")
        return int(cr.split("/")[-1]) if "/" in cr and cr.split("/")[-1].isdigit() else None
    finally:
        if own:
            client.close()


def fetch_3w(progress: Progress | None = None, verify: bool = True) -> Path:
    """Resumable download of the zip; records size + SHA-256 in ``raw/3w_manifest.json``."""
    dest = raw_dir() / ZIP_NAME
    size = remote_size()
    download(URL, dest, expected_size=size, progress=progress)
    man_path = raw_dir() / "3w_manifest.json"
    man = read_manifest(man_path)
    if verify:
        digest = sha256_file(dest)
        if man.get("sha256") and man["sha256"] != digest:
            raise RuntimeError("3W zip checksum differs from the recorded one; delete and re-download")
        man.update(sha256=digest, size=dest.stat().st_size, url=URL)
        write_manifest(man_path, man)
    update_licenses(raw_dir(), "R1 Petrobras 3W v2.0.0", LICENCE)
    return dest


def parse_instance(name: str) -> dict:
    stem = Path(name).stem
    m = _INST.search(stem)
    origin = {"well": "real"}.get(m.group("origin").lower(), m.group("origin").lower()) if m else "unknown"
    return {"instance_id": stem, "origin": origin}


def _class_of(member: str) -> int | None:
    for part in Path(member).parts[:-1]:
        if part.isdigit() and int(part) in EVENT_NAMES:
            return int(part)
    return None


def normalise_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df.index.name and df.index.name.lower() == "timestamp":
        df = df.reset_index()
    df = df.rename(columns={c: c.lower().replace("-", "_") for c in df.columns})
    if "timestamp" in df:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    for c in df.columns:
        if c != "timestamp" and pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].astype("float32")
    return df


def convert_3w(
    zip_path: Path | None = None,
    out_dir: Path | None = None,
    sample_per_class: int = 40,
    sample_freq: str = "60s",
    limit: int | None = None,
    seed: int = 0,
) -> dict[str, Path]:
    """Convert every ``*.parquet`` instance in the zip into ``processed/threew/class=N/`` (float32, zstd),
    write the index ``threew_events.parquet`` and the compact ``threew_sample.parquet`` (a few hundred
    instances covering every class, real instances first, down-sampled to ``sample_freq`` means)."""
    zip_path = zip_path or raw_dir() / ZIP_NAME
    out_dir = out_dir or processed_dir()
    base = out_dir / "threew"
    base.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    with zipfile.ZipFile(zip_path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".parquet") and _class_of(n) is not None)
        if limit:
            members = members[:limit]
        for n in members:
            cls = _class_of(n)
            assert cls is not None
            info = parse_instance(n)
            dest = base / f"class={cls}" / f"{info['instance_id']}.parquet"
            if dest.exists():
                meta = pq.ParquetFile(dest).metadata
                ts = pd.read_parquet(dest, columns=["timestamp"])["timestamp"]
                rows.append(_index_row(info, cls, meta.num_rows, ts, dest, base))
                continue
            df = normalise_frame(pd.read_parquet(io.BytesIO(z.read(n))))
            df["instance_id"] = info["instance_id"]
            df["event_class"] = np.int8(cls)
            dest.parent.mkdir(exist_ok=True)
            tmp = dest.with_suffix(".tmp")
            df.to_parquet(tmp, index=False, compression="zstd", compression_level=9)
            tmp.rename(dest)
            rows.append(_index_row(info, cls, len(df), df["timestamp"], dest, base))
    idx = pd.DataFrame(rows)
    idx["source"] = "real"
    idx["licence"] = "CC BY 4.0"
    idx_path = out_dir / "threew_events.parquet"
    idx.to_parquet(idx_path, index=False)
    sample_path = out_dir / "threew_sample.parquet"
    make_sample(idx, base, sample_path, sample_per_class, sample_freq, seed)
    return {"index": idx_path, "sample": sample_path, "dir": base}


def _index_row(info: dict, cls: int, n: int, ts: pd.Series, dest: Path, base: Path) -> dict:
    return {
        "instance_id": info["instance_id"], "event_class": cls, "event_name": EVENT_NAMES[cls],
        "origin": info["origin"], "n_rows": int(n),
        "start": ts.min() if len(ts) else pd.NaT, "end": ts.max() if len(ts) else pd.NaT,
        "path": str(dest.relative_to(base.parent)),
    }


def make_sample(idx: pd.DataFrame, base: Path, out: Path, per_class: int, freq: str, seed: int) -> None:
    rng = np.random.default_rng(seed)
    frames = []
    for cls, g in idx.groupby("event_class"):
        real = g[g.origin == "real"]
        rest = g[g.origin != "real"]
        pick = list(real.index)
        rng.shuffle(pick)
        pick = pick[:per_class]
        if len(pick) < per_class:
            more = list(rest.index)
            rng.shuffle(more)
            pick += more[: per_class - len(pick)]
        for i in pick:
            df = pd.read_parquet(base.parent / idx.loc[i, "path"])
            num = df.select_dtypes("number").columns.difference(["event_class"])
            rs = df.set_index("timestamp")[list(num)].resample(freq).mean()
            if "class" in df:  # per-sample label: modal class in the window
                rs["class"] = df.set_index("timestamp")["class"].resample(freq).max()
            rs = rs.dropna(how="all").reset_index()
            rs["instance_id"] = idx.loc[i, "instance_id"]
            rs["event_class"] = np.int8(cls)
            rs["origin"] = idx.loc[i, "origin"]
            frames.append(rs)
    if frames:
        s = pd.concat(frames, ignore_index=True)
        s["source"] = "real"
        for c in s.columns:
            if pd.api.types.is_float_dtype(s[c]):
                s[c] = s[c].astype("float32")
        pa_tbl = pa.Table.from_pandas(s, preserve_index=False)
        pq.write_table(pa_tbl, out, compression="zstd")


def utcnow() -> str:
    return datetime.now(UTC).isoformat()
