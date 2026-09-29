"""Small helpers that reproduce JavaScript numeric semantics used by the browser twin."""

from __future__ import annotations

import math
import re
from dataclasses import fields, is_dataclass
from typing import Any

TAU = math.pi * 2


def clamp(v: float, a: float, b: float) -> float:
    return a if v < a else b if v > b else v


def smooth(t: float) -> float:
    t = clamp(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def fin(v: Any, d: float = 0.0) -> float:
    """JS ``Number.isFinite(v) ? v : d`` (None counts as non-finite, like undefined/NaN)."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return d
    return f if math.isfinite(f) else d


def js_round(x: float) -> int:
    """JS ``Math.round`` (half rounds up), unlike Python's banker's rounding."""
    return math.floor(x + 0.5)


def js_mod(a: float, b: float) -> float:
    """JS ``%`` on floats (sign follows the dividend)."""
    return math.fmod(a, b)


def to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


_CAMEL_RE = re.compile(r"_([a-z0-9])")


def to_json_value(obj: Any, overrides: dict[str, str] | None = None) -> Any:
    """Recursively convert dataclasses to camelCase dicts (the JS wire format)."""
    if is_dataclass(obj) and not isinstance(obj, type):
        ov = getattr(obj, "_JSON_KEYS", {}) or {}
        return {ov.get(f.name, to_camel(f.name)): to_json_value(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, (list, tuple)):
        return [to_json_value(v) for v in obj]
    if isinstance(obj, dict):
        return {k: to_json_value(v) for k, v in obj.items()}
    if hasattr(obj, "tolist"):
        return obj.tolist()
    return obj


class JsonMixin:
    """Adds ``to_json()`` emitting the camelCase keys the JS twin returns."""

    _JSON_KEYS: dict[str, str] = {}

    def to_json(self) -> Any:
        return to_json_value(self)
