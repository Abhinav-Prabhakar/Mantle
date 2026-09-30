"""Token / cost estimates for LLM synthesis runs (no API calls)."""

from __future__ import annotations

import os
from typing import Any

from .runner import render_prompts
from .sampling import Context
from .spec import get_spec, load_specs

# USD per million tokens (input, output). ASSUMPTIONS for planning only: override with
# MANTLE_LLM_PRICE_IN / MANTLE_LLM_PRICE_OUT.
DEFAULT_PRICE = (3.0, 15.0)
CHARS_PER_TOKEN = 4.0


def prices() -> tuple[float, float]:
    return (float(os.environ.get("MANTLE_LLM_PRICE_IN", DEFAULT_PRICE[0])),
            float(os.environ.get("MANTLE_LLM_PRICE_OUT", DEFAULT_PRICE[1])))


def estimate(spec_key: str = "all", n: int | None = None, model: str = "claude-sonnet-5-5",
             context: Context | None = None) -> list[dict]:
    ctx = context or Context.load()
    keys = list(load_specs()) if spec_key.lower() == "all" else [get_spec(spec_key).id]
    p_in, p_out = prices()
    rows: list[dict[str, Any]] = []
    for k in keys:
        spec = get_spec(k)
        calls = n or spec.suggested_n
        sample = render_prompts(spec, 5, ctx)
        avg_in = sum(len(s["system"]) + len(s["user"]) for s in sample) / len(sample) / CHARS_PER_TOKEN
        t_in, t_out = avg_in * calls, spec.est_output_tokens * calls
        rows.append({"spec": spec.id, "name": spec.name, "model": model, "calls": calls,
                     "input_tokens": int(t_in), "output_tokens": int(t_out),
                     "usd": round(t_in / 1e6 * p_in + t_out / 1e6 * p_out, 2),
                     "price_usd_per_mtok": [p_in, p_out]})
    if len(rows) > 1:
        rows.append({"spec": "TOTAL", "calls": sum(r["calls"] for r in rows),
                     "input_tokens": sum(r["input_tokens"] for r in rows),
                     "output_tokens": sum(r["output_tokens"] for r in rows),
                     "usd": round(sum(r["usd"] for r in rows), 2)})
    return rows
