"""Paste-and-return packs: render batches of L1-L13 items as self-contained Markdown for a chat LLM."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ..paths import packs_dir
from ..synth.common import SEED
from .sampling import Context, sample_variables
from .spec import Spec, get_spec, load_specs, system_prompt

# spec -> (items per batch, starter items). Big records get small batches, short ones big batches.
DEFAULTS: dict[str, tuple[int, int]] = {
    "L1": (10, 100), "L2": (15, 150), "L3": (12, 240), "L4": (20, 200), "L5": (20, 300), "L6": (20, 200),
    "L7": (30, 300), "L8": (25, 300), "L9": (12, 120), "L10": (20, 200), "L11": (10, 50), "L12": (25, 250),
    "L13": (15, 150),
}
ITEM_ID_RE = re.compile(r"^(L\d+)-(\d+)$")


def item_id(spec_id: str, idx: int) -> str:
    return f"{spec_id}-{idx:05d}"


def resolve_dir(out: str | Path | None) -> Path:
    return Path(out) if out else packs_dir()


def read_manifest(pack_dir: Path) -> list[dict[str, Any]]:
    p = pack_dir / "manifest.jsonl"
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def status_path(pack_dir: Path) -> Path:
    return pack_dir / "status.json"


def read_status(pack_dir: Path) -> dict[str, dict[str, str]]:
    p = status_path(pack_dir)
    return json.loads(p.read_text()) if p.exists() else {}


def _schema_block(spec: Spec) -> str:
    js = spec.json_schema()
    props = {"item_id": {"type": "string", "description": "copy the item_id of the item exactly"}, **js["properties"]}
    js = {**js, "properties": props, "required": ["item_id", *js["required"]]}
    lines = ["{", '  "type": "object", "additionalProperties": false,', f'  "required": {json.dumps(js["required"])},',
             '  "properties": {']
    items = [f"    {json.dumps(k)}: {json.dumps(v)}" for k, v in props.items()]
    lines.append(",\n".join(items))
    lines += ["  }", "}"]
    return "\n".join(lines)


def _constraints(spec: Spec) -> str:
    c = []
    for chain in spec.checks.get("monotone_desc", []):
        c.append("- " + " >= ".join(chain))
    for a, b in spec.checks.get("ordered_ascending", []):
        c.append(f"- {a} <= {b}")
    return "\n".join(["", "Extra constraints:", *c]) if c else ""


def render_batch(spec: Spec, title: str, items: list[dict[str, Any]], pack_dir_name: str, notes: dict[str, str] | None = None) -> str:
    n = len(items)
    ids = items[0]["item_id"] + (f" .. {items[-1]['item_id']}" if n > 1 else "")
    reply = f"llm-packs/{spec.id}/replies/{title}.json"
    out = [
        f"# {spec.id} {spec.name} - {title.split('_', 1)[1].replace('_', ' ')} ({n} items)",
        "",
        "## How to use",
        "1. Start a NEW chat with your LLM and paste this ENTIRE file as the message.",
        f"2. It must reply with ONE JSON array only: exactly {n} objects, no prose, no markdown fences.",
        f"3. Save the reply as `{reply}` (any *.json / *.md / *.txt name inside `replies/` works).",
        "4. Import everything with: `cd backend && uv run mantle-data llm import ../llm-packs`",
        "",
        f"Items in this file: {ids} (each has an `item_id` you must echo).",
        "",
        "## System prompt (applies to every item)",
        system_prompt().strip(),
        "",
        "## JSON schema for ONE record",
        "```json",
        _schema_block(spec),
        "```" + _constraints(spec),
        "",
        f"## Items ({n})",
        "Write one record per item, following the instruction under each item_id.",
        "",
    ]
    for it in items:
        out += [f"### item_id: {it['item_id']}", spec.render(it["variables"]).strip()]
        if notes and it["item_id"] in notes:
            out.append(f"(A previous attempt was rejected: {notes[it['item_id']]} - fix this.)")
        out.append("")
    out += [
        "## Output contract",
        f"Return a JSON array of exactly {n} objects, in the order listed above. Each object has `item_id` "
        f"(copied exactly) plus every field of the schema, and no other keys.",
        "No prose, no markdown fences, no comments - the reply must start with `[` and end with `]`.",
        "",
    ]
    return "\n".join(out)


def pack(spec_key: str, n: int | None = None, batch: int | None = None, seed: int = SEED,
         out: str | Path | None = None, ctx: Context | None = None) -> dict[str, Any]:
    """Append ``n`` NEW items (continuing after what the manifest already holds) as batch files."""
    spec = get_spec(spec_key)
    d_batch, d_n = DEFAULTS.get(spec.id, (10, 100))
    n = d_n if n is None else n
    batch = d_batch if batch is None else batch
    if n < 1 or batch < 1:
        raise ValueError("n and batch must be >= 1")
    ctx = ctx or Context.load()
    pdir = resolve_dir(out) / spec.id
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "replies").mkdir(exist_ok=True)
    mani = read_manifest(pdir)
    start = max((m["idx"] for m in mani), default=-1) + 1
    b0 = max((m["batch"] for m in mani), default=0)
    files, rows = [], []
    for bi, lo in enumerate(range(0, n, batch), start=1):
        b = b0 + bi
        items = []
        for i in range(start + lo, start + min(lo + batch, n)):
            v = sample_variables(spec.id, ctx, i, seed)
            spec.render(v)   # raises on any missing variable
            it = {"item_id": item_id(spec.id, i), "idx": i, "variables": v}
            items.append(it)
            rows.append({"item_id": it["item_id"], "spec": spec.id, "idx": i, "batch": b, "seed": seed, "variables": v})
        f = pdir / f"{spec.id}_batch_{b:03d}.md"
        f.write_text(render_batch(spec, f"{spec.id}_batch_{b:03d}", items, pdir.name))
        files.append(str(f))
    with open(pdir / "manifest.jsonl", "a") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return {"spec": spec.id, "items": len(rows), "batches": len(files), "files": files}


def pack_retry(spec_key: str, batch: int | None = None, out: str | Path | None = None) -> dict[str, Any]:
    """Regenerate only failed/missing item_ids (per status.json) as ``<spec>_retry_NNN.md`` files."""
    spec = get_spec(spec_key)
    batch = batch or DEFAULTS.get(spec.id, (10, 100))[0]
    pdir = resolve_dir(out) / spec.id
    for old in pdir.glob(f"{spec.id}_retry_*.md"):
        old.unlink()
    st = read_status(pdir)
    by_id = {m["item_id"]: m for m in read_manifest(pdir)}
    bad = [i for i in sorted(st) if st[i]["status"] in ("rejected", "missing") and i in by_id]
    files = []
    for k, lo in enumerate(range(0, len(bad), batch), start=1):
        chunk = bad[lo: lo + batch]
        items = [{"item_id": i, "idx": by_id[i]["idx"], "variables": by_id[i]["variables"]} for i in chunk]
        notes = {i: st[i].get("reason", "") for i in chunk if st[i]["status"] == "rejected"}
        title = f"{spec.id}_retry_{k:03d}"
        f = pdir / f"{title}.md"
        f.write_text(render_batch(spec, title, items, pdir.name, notes))
        files.append(str(f))
    return {"spec": spec.id, "items": len(bad), "batches": len(files), "files": files, "item_ids": bad}


def spec_ids(key: str) -> list[str]:
    return list(load_specs()) if key.lower() == "all" else [get_spec(key).id]
