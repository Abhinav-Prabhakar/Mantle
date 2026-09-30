"""Resumable, retrying downloads with checksums (used by every real-data fetcher)."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from pathlib import Path

import httpx

CHUNK = 1 << 20
Progress = Callable[[int, int | None], None]


def sha256_file(path: Path, chunk: int = CHUNK) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def download(
    url: str,
    dest: Path,
    *,
    expected_size: int | None = None,
    max_retries: int = 20,
    backoff: float = 2.0,
    max_backoff: float = 60.0,
    progress: Progress | None = None,
    client: httpx.Client | None = None,
    headers: dict[str, str] | None = None,
) -> Path:
    """Download ``url`` to ``dest`` resuming a partial file with HTTP Range and retrying with backoff.

    Idempotent: a complete file (size == ``expected_size`` or the server-reported length) is left alone.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    own = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=httpx.Timeout(30.0, read=60.0))
    attempt = 0
    try:
        while True:
            have = dest.stat().st_size if dest.exists() else 0
            if expected_size is not None and have == expected_size:
                return dest
            try:
                hdr = dict(headers or {})
                if have:
                    hdr["Range"] = f"bytes={have}-"
                with client.stream("GET", url, headers=hdr) as r:
                    if r.status_code == 416:  # range not satisfiable: already complete
                        return dest
                    r.raise_for_status()
                    mode = "ab"
                    if have and r.status_code != 206:  # server ignored Range: restart
                        mode, have = "wb", 0
                    clen = r.headers.get("content-length")
                    total = have + int(clen) if clen is not None else expected_size
                    done = have
                    with open(dest, mode) as f:
                        for block in r.iter_bytes(CHUNK):
                            f.write(block)
                            done += len(block)
                            if progress:
                                progress(done, total)
                    if total is not None and done < total:
                        raise httpx.ReadError("short read")
                    return dest
            except (httpx.HTTPError, OSError) as e:
                attempt += 1
                if attempt > max_retries:
                    raise
                time.sleep(min(max_backoff, backoff * 2 ** (attempt - 1)) if backoff else 0)
                if isinstance(e, httpx.HTTPStatusError) and e.response.status_code in (400, 401, 403, 404):
                    raise
    finally:
        if own:
            client.close()


def read_manifest(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def write_manifest(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def update_licenses(raw: Path, key: str, text: str) -> None:
    """Idempotently maintain a section per dataset in ``LICENSES.md``."""
    p = raw / "LICENSES.md"
    sections: dict[str, str] = {}
    if p.exists():
        cur = None
        for line in p.read_text().splitlines():
            if line.startswith("## "):
                cur = line[3:].strip()
                sections[cur] = ""
            elif cur is not None:
                sections[cur] += line + "\n"
    sections[key] = text.strip() + "\n"
    body = "# Data licences and citations\n\n" + "\n".join(f"## {k}\n{v}" for k, v in sorted(sections.items()))
    p.write_text(body)
