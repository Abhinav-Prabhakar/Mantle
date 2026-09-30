"""LLM providers: Anthropic SDK, any OpenAI-compatible endpoint, and a scriptable fake for tests."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Completion:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0


class Provider(Protocol):
    name: str

    def complete(self, system: str, user: str, model: str, max_tokens: int = 2048,
                 temperature: float = 1.0) -> Completion: ...


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str | None = None):
        import anthropic

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        self.client = anthropic.Anthropic(api_key=key)

    def complete(self, system, user, model, max_tokens=2048, temperature=1.0) -> Completion:
        r = self.client.messages.create(model=model, max_tokens=max_tokens, temperature=temperature, system=system,
                                        messages=[{"role": "user", "content": user}])
        text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
        return Completion(text, r.usage.input_tokens, r.usage.output_tokens)


class OpenAICompatProvider:
    name = "openai-compatible"

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        import openai

        self.client = openai.OpenAI(base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
                                    api_key=api_key or os.environ.get("OPENAI_API_KEY") or "none")

    def complete(self, system, user, model, max_tokens=2048, temperature=1.0) -> Completion:
        r = self.client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=temperature,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        u = r.usage
        return Completion(r.choices[0].message.content or "", getattr(u, "prompt_tokens", 0),
                          getattr(u, "completion_tokens", 0))


class FakeProvider:
    """Deterministic offline provider. ``script`` maps (call number, spec-agnostic prompt) -> text."""

    name = "fake"

    def __init__(self, respond: Callable[[int, str, str], str] | None = None):
        self.respond = respond
        self.calls = 0
        self.prompts: list[str] = []

    def complete(self, system, user, model, max_tokens=2048, temperature=1.0) -> Completion:
        self.calls += 1
        self.prompts.append(user)
        text = self.respond(self.calls, system, user) if self.respond else "{}"
        return Completion(text, len(system + user) // 4, len(text) // 4)


def make_provider(name: str, base_url: str | None = None) -> Provider:
    if name == "anthropic":
        return AnthropicProvider()
    if name in ("openai-compatible", "openai"):
        return OpenAICompatProvider(base_url)
    raise ValueError(f"unknown provider {name!r}")
