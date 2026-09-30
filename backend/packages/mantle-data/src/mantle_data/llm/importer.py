"""Import chat-LLM replies (JSON arrays, possibly wrapped in fences/prose) back into data/llm + DuckDB."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ..paths import llm_dir
from .dedupe import Deduper
from .pack import ITEM_ID_RE, read_manifest, read_status, resolve_dir, status_path
from .runner import _read_jsonl, record_text
from .spec import get_spec, validate_record

_PACK_FILE = re.compile(r"_(batch|retry)_\d+\.md$")
_SUFFIXES = {".json", ".md", ".txt"}


def parse_reply(text: str) -> list[Any]:
    """Every JSON object found in the reply: arrays are flattened; tolerant of fences and prose."""
    dec = json.JSONDecoder()
    found: list[Any] = []
    pos = 0
    while pos < len(text):
        m = re.search(r"[\[{]", text[pos:])
        if not m:
            break
        i = pos + m.start()
        try:
            obj, end = dec.raw_decode(text, i)
        except json.JSONDecodeError:
            pos = i + 1
            continue
        pos = end
        if isinstance(obj, list):
            found.extend(obj)
        elif isinstance(obj, dict):
            lists = [v for v in obj.values() if isinstance(v, list) and v and all(isinstance(x, dict) for x in v)]
            if "item_id" not in obj and len(lists) == 1:      # {"items": [...]} wrapper
                found.extend(lists[0])
            else:
                found.append(obj)
    return found


def collect_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    out = []
    for f in sorted(path.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in _SUFFIXES or f.name == "README.md":
            continue
        if _PACK_FILE.search(f.name) and f.parent.name != "replies":
            continue    # the pasteable pack itself, not a reply
        out.append(f)
    return out


def import_replies(path: str | Path, packs: str | Path | None = None, load_db: bool = True) -> dict[str, Any]:
    root = resolve_dir(packs)
    files = collect_files(Path(path))
    report: dict[str, Any] = {"files": len(files), "specs": {}, "unparseable": [], "db_rows": None}
    per_spec: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for f in files:
        try:
            objs = parse_reply(f.read_text(errors="replace"))
        except Exception as e:  # noqa: BLE001
            report["unparseable"].append(f"{f}: {e}")
            continue
        if not objs:
            report["unparseable"].append(f"{f}: no JSON array found")
            continue
        for o in objs:
            iid = o.get("item_id") if isinstance(o, dict) else None
            m = ITEM_ID_RE.match(iid) if isinstance(iid, str) else None
            if not m:
                r = report["specs"].setdefault("?", _empty())
                r["rejected"].append({"item_id": str(iid), "reason": "missing or malformed item_id", "file": f.name})
                continue
            per_spec[m.group(1)].append((f.name, o))
    for spec_id, entries in per_spec.items():
        report["specs"][spec_id] = _import_spec(spec_id, entries, root)
    if load_db and any(r["accepted"] for r in report["specs"].values()):
        try:
            from .. import db

            report["db_rows"] = db.load_llm()
        except Exception as e:  # noqa: BLE001  (e.g. the dev API holds the DuckDB lock)
            report["db_error"] = f"DuckDB not updated ({str(e)[:120]}); run `uv run mantle-data db load` later"
    return report


def _empty() -> dict[str, Any]:
    return {"accepted": [], "rejected": [], "duplicates": [], "already_imported": [], "missing": []}


def _import_spec(spec_id: str, entries: list[tuple[str, dict]], root: Path) -> dict[str, Any]:
    spec = get_spec(spec_id)
    pdir = root / spec_id
    by_id = {m["item_id"]: m for m in read_manifest(pdir)}
    out = llm_dir() / f"{spec_id}.jsonl"
    existing = _read_jsonl(out)
    have = {str(r["item_id"]) for r in existing if r.get("item_id")}
    dd = Deduper()
    for r in existing:
        dd.add(record_text(r["record"]))
    rep = _empty()
    seen: set[str] = set()
    rows = []
    touched_batches: set[int] = set()
    for fname, obj in entries:
        iid = obj["item_id"]
        if iid not in by_id:
            rep["rejected"].append({"item_id": iid, "reason": f"unknown item_id (not in {spec_id}/manifest.jsonl)",
                                    "file": fname})
            continue
        touched_batches.add(by_id[iid]["batch"])
        if iid in have:
            rep["already_imported"].append(iid)
            seen.add(iid)
            continue
        if iid in seen:
            rep["duplicates"].append({"item_id": iid, "reason": "item_id repeated in replies", "file": fname})
            continue
        seen.add(iid)
        body = {k: v for k, v in obj.items() if k != "item_id"}
        try:
            rec = validate_record(spec, body)
        except (ValidationError, ValueError) as e:
            rep["rejected"].append({"item_id": iid, "reason": _reason(e), "file": fname})
            continue
        if not dd.add(record_text(rec)):
            rep["duplicates"].append({"item_id": iid, "reason": "near-duplicate of an existing record", "file": fname})
            continue
        m = by_id[iid]
        rows.append({"idx": m["idx"], "spec": spec_id, "item_id": iid, "model": "manual-chat", "provider": "manual",
                     "created_at": datetime.now(UTC).isoformat(), "attempts": 1, "variables": m["variables"],
                     "record": rec, "source": "llm_synthetic"})
        rep["accepted"].append(iid)
    if rows:
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and out.stat().st_size and not out.read_bytes().endswith(b"\n"):
            with open(out, "a") as f:
                f.write("\n")
        with open(out, "a") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    done = have | set(rep["accepted"])
    dup_ids = {d["item_id"] for d in rep["duplicates"]}
    for m in by_id.values():
        if m["batch"] in touched_batches and m["item_id"] not in seen and m["item_id"] not in done:
            rep["missing"].append(m["item_id"])
    st = read_status(pdir)
    for iid in done | dup_ids:
        st.pop(iid, None)
    for r in rep["rejected"]:
        if r["item_id"] in by_id:
            st[r["item_id"]] = {"status": "rejected", "reason": r["reason"]}
    for iid in rep["missing"]:
        st.setdefault(iid, {"status": "missing", "reason": "not in the reply"})
    if pdir.exists():
        status_path(pdir).write_text(json.dumps(st, indent=1, sort_keys=True) + "\n")
    return rep


def _reason(e: Exception) -> str:
    if isinstance(e, ValidationError):
        return "; ".join(f"{'.'.join(map(str, x['loc'])) or 'record'}: {x['msg']}" for x in e.errors())[:300]
    return str(e)[:300]


def format_report(rep: dict[str, Any]) -> str:
    lines = [f"files read: {rep['files']}"]
    for u in rep["unparseable"]:
        lines.append(f"  UNPARSEABLE {u}")
    for sid, r in sorted(rep["specs"].items()):
        lines.append(f"{sid}: accepted {len(r['accepted'])}, rejected {len(r['rejected'])}, "
                     f"duplicates {len(r['duplicates'])}, already imported {len(r['already_imported'])}, "
                     f"missing {len(r['missing'])}")
        for x in r["rejected"] + r["duplicates"]:
            lines.append(f"  - {x['item_id']}: {x['reason']}  ({x['file']})")
        if r["missing"]:
            lines.append(f"  - missing from replies: {', '.join(r['missing'])}")
        if r["rejected"] or r["missing"]:
            lines.append(f"  -> re-paste only these: uv run mantle-data llm pack {sid} --retry-failed")
    if rep.get("db_rows") is not None:
        lines.append(f"DuckDB llm_records: {rep['db_rows']} rows")
    if rep.get("db_error"):
        lines.append(rep["db_error"])
    return "\n".join(lines)
