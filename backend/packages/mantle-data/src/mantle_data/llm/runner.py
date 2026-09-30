"""Resumable, concurrent LLM synthesis runner with retries, validation and dedupe."""

from __future__ import annotations

import json
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ..paths import llm_dir
from ..synth.common import SEED
from .dedupe import Deduper
from .providers import Provider, make_provider
from .sampling import Context, sample_variables
from .spec import Spec, get_spec, system_prompt, validate_record

MAX_INVALID_ATTEMPTS = 3
MAX_TRANSIENT_RETRIES = 6
_sleep = time.sleep       # patched in tests


def extract_json(text: str) -> Any:
    """Parse a model reply as JSON (tolerates code fences / leading prose)."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, re.S)
        if not m:
            raise
        return json.loads(m.group(0))


def record_text(rec: dict) -> str:
    return " ".join(str(v) for v in rec.values())


def out_path(spec: Spec, directory: Path | None = None) -> Path:
    return (directory or llm_dir()) / f"{spec.id}.jsonl"


def _read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue      # a torn final line from an interrupted run
    return out


def render_prompts(spec: Spec, n: int, ctx: Context, seed: int = SEED, start: int = 0) -> list[dict[str, Any]]:
    res = []
    for i in range(start, start + n):
        v = sample_variables(spec.id, ctx, i, seed)
        res.append({"idx": i, "variables": v, "system": system_prompt(), "user": spec.full_prompt(v)})
    return res


def _call(provider: Provider, spec: Spec, item: dict, model: str, temperature: float) -> dict:
    """One item: transient-error retries with backoff; invalid output regenerated up to 3 times."""
    tok_in = tok_out = 0
    last = ""
    for attempt in range(1, MAX_INVALID_ATTEMPTS + 1):
        transient = 0
        while True:
            try:
                c = provider.complete(item["system"], item["user"], model, 2048, temperature)
                break
            except Exception as e:   # noqa: BLE001  (SDK errors vary by provider)
                transient += 1
                if transient > MAX_TRANSIENT_RETRIES:
                    return {"ok": False, "reason": f"provider error: {e}", "attempts": attempt,
                            "in": tok_in, "out": tok_out}
                _sleep(min(60.0, 2.0 ** transient) * (0.5 + random.random() / 2))
        tok_in += c.input_tokens
        tok_out += c.output_tokens
        try:
            rec = validate_record(spec, extract_json(c.text))
            return {"ok": True, "record": rec, "attempts": attempt, "in": tok_in, "out": tok_out}
        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            last = str(e)[:300]
    return {"ok": False, "reason": f"invalid after {MAX_INVALID_ATTEMPTS} attempts: {last}",
            "attempts": MAX_INVALID_ATTEMPTS, "in": tok_in, "out": tok_out}


def run(spec_key: str, n: int, model: str = "claude-sonnet-5-5", provider: str | Provider = "anthropic",
        concurrency: int = 8, dry_run: bool = False, seed: int = SEED, base_url: str | None = None,
        directory: Path | None = None, context: Context | None = None, temperature: float = 1.0) -> dict:
    spec = get_spec(spec_key)
    ctx = context or Context.load()
    if dry_run:
        prompts = render_prompts(spec, min(n, 3), ctx, seed)
        return {"spec": spec.id, "dry_run": True, "n": n, "rendered": len(prompts), "prompts": prompts}
    prov = make_provider(provider, base_url) if isinstance(provider, str) else provider
    path = out_path(spec, directory)
    path.parent.mkdir(parents=True, exist_ok=True)
    rej_path = path.with_suffix(".rejects.jsonl")
    done = _read_jsonl(path)
    rejected = _read_jsonl(rej_path)
    seen_idx = {r["idx"] for r in done} | {r["idx"] for r in rejected}
    dd = Deduper()
    for r in done:
        dd.add(record_text(r["record"]))
    for fp in (path, rej_path):     # an interrupted run may leave a torn last line: start a fresh one
        if fp.exists() and fp.stat().st_size and not fp.read_bytes().endswith(b"\n"):
            with open(fp, "a") as f:
                f.write("\n")
    pending = [i for i in range(n) if i not in seen_idx]
    stats: dict[str, Any] = {"spec": spec.id, "requested": n, "already_done": len(seen_idx & set(range(n))), "generated": 0,
             "invalid": 0, "duplicates": 0, "input_tokens": 0, "output_tokens": 0, "path": str(path)}
    lock = threading.Lock()
    by_idx = {i: render_prompts(spec, 1, ctx, seed, start=i)[0] for i in pending}
    with open(path, "a") as f_ok, open(rej_path, "a") as f_rej, ThreadPoolExecutor(max(1, concurrency)) as ex:
        futs = {ex.submit(_call, prov, spec, by_idx[i], model, temperature): i for i in pending}
        for fut in as_completed(futs):
            i = futs[fut]
            res = fut.result()
            with lock:
                stats["input_tokens"] += res["in"]
                stats["output_tokens"] += res["out"]
                base = {"idx": i, "spec": spec.id, "model": model, "provider": prov.name,
                        "created_at": datetime.now(UTC).isoformat(), "attempts": res["attempts"]}
                if not res["ok"]:
                    stats["invalid"] += 1
                    f_rej.write(json.dumps({**base, "reason": res["reason"]}) + "\n")
                    f_rej.flush()
                elif not dd.add(record_text(res["record"])):
                    stats["duplicates"] += 1
                    f_rej.write(json.dumps({**base, "reason": "duplicate"}) + "\n")
                    f_rej.flush()
                else:
                    stats["generated"] += 1
                    f_ok.write(json.dumps({**base, "variables": by_idx[i]["variables"], "record": res["record"],
                                           "source": "llm_synthetic"}) + "\n")
                    f_ok.flush()
    return stats
