"""Prompt specs (YAML) -> rendered prompts, JSON schema and a pydantic validator."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model, model_validator

from ..paths import prompts_dir

_JSON_TYPES = {"str": "string", "int": "integer", "float": "number", "bool": "boolean"}


@dataclass
class Spec:
    id: str
    name: str
    suggested_n: int
    user_template: str
    fields: list[dict[str, Any]]
    variables: list[str] = field(default_factory=list)
    sampled_from: list[str] = field(default_factory=list)
    records_per_call: int = 1
    est_output_tokens: int = 400
    checks: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    @property
    def key(self) -> str:
        return self.id

    def render(self, variables: dict[str, Any]) -> str:
        missing = [v for v in self.variables if v not in variables]
        if missing:
            raise KeyError(f"{self.id}: missing template variables {missing}")
        return self.user_template.format(**variables)

    def json_schema(self) -> dict[str, Any]:
        props: dict[str, Any] = {}
        for f in self.fields:
            t = f["type"]
            if t.startswith("list["):
                inner = _JSON_TYPES[t[5:-1]]
                p: dict[str, Any] = {"type": "array", "items": {"type": inner}}
                if "min_items" in f:
                    p["minItems"] = f["min_items"]
                if "max_items" in f:
                    p["maxItems"] = f["max_items"]
            else:
                p = {"type": _JSON_TYPES[t]}
                if "enum" in f:
                    p["enum"] = f["enum"]
                if "min" in f:
                    p["minimum"] = f["min"]
                if "max" in f:
                    p["maximum"] = f["max"]
            if f.get("description"):
                p["description"] = f["description"]
            props[f["name"]] = p
        return {"type": "object", "properties": props, "required": [f["name"] for f in self.fields],
                "additionalProperties": False}

    def model(self) -> type[BaseModel]:
        return _build_model(self)

    def full_prompt(self, variables: dict[str, Any]) -> str:
        import json

        return (self.render(variables) + "\n\nReturn ONE JSON object (no prose, no code fences) matching this "
                f"JSON schema:\n{json.dumps(self.json_schema())}")


def _build_model(spec: Spec) -> type[BaseModel]:
    defs: dict[str, Any] = {}
    py = {"str": str, "int": int, "float": float, "bool": bool}
    for f in spec.fields:
        t = f["type"]
        kw: dict[str, Any] = {}
        if t.startswith("list["):
            typ: Any = list[py[t[5:-1]]]  # type: ignore[misc]
            if "min_items" in f:
                kw["min_length"] = f["min_items"]
            if "max_items" in f:
                kw["max_length"] = f["max_items"]
        else:
            typ = py[t]
            if "min" in f:
                kw["ge"] = f["min"]
            if "max" in f:
                kw["le"] = f["max"]
            if t == "str":
                kw["min_length"] = 1
        defs[f["name"]] = (typ, Field(..., **kw))
    checks = spec.checks

    class Base(BaseModel):
        model_config = ConfigDict(extra="forbid")

        @model_validator(mode="after")
        def _checks(self):
            for chain in checks.get("monotone_desc", []):
                vals = [getattr(self, k) for k in chain]
                if any(a < b for a, b in zip(vals, vals[1:], strict=False)):
                    raise ValueError(f"{chain} must decrease")
            for a, b in checks.get("ordered_ascending", []):
                if getattr(self, a) > getattr(self, b):
                    raise ValueError(f"{a} must not exceed {b}")
            enums = {f["name"]: f["enum"] for f in spec.fields if "enum" in f}
            for k, allowed in enums.items():
                if getattr(self, k) not in allowed:
                    raise ValueError(f"{k} not in {allowed}")
            return self

    return create_model(f"{spec.id}Record", __base__=Base, **defs)


def load_spec(path: Path) -> Spec:
    d = yaml.safe_load(path.read_text())
    return Spec(**d)


@lru_cache(maxsize=1)
def _all() -> dict[str, Spec]:
    def order(path: Path) -> int:
        m = re.match(r"L(\d+)_", path.name)
        return int(m.group(1)) if m else 0

    specs = {}
    for p in sorted(prompts_dir().glob("L*_*.yaml"), key=order):
        s = load_spec(p)
        specs[s.id] = s
    return specs


def load_specs() -> dict[str, Spec]:
    return dict(_all())


def get_spec(key: str) -> Spec:
    specs = _all()
    k = key.upper()
    if k in specs:
        return specs[k]
    for s in specs.values():
        if s.name == key:
            return s
    raise KeyError(f"unknown spec {key!r}; available: {', '.join(specs)}")


@lru_cache(maxsize=1)
def system_prompt() -> str:
    return yaml.safe_load((prompts_dir() / "_system.yaml").read_text())["system"]


def validate_record(spec: Spec, obj: Any) -> dict[str, Any]:
    """Validate a parsed JSON object; returns the normalised dict or raises ValidationError."""
    return spec.model().model_validate(obj).model_dump()


__all__ = ["Spec", "ValidationError", "get_spec", "load_specs", "system_prompt", "validate_record"]
