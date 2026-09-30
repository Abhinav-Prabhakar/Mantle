"""Near-duplicate detection for text records (exact hash + MinHash-LSH on word 3-shingles)."""

from __future__ import annotations

import hashlib
import re

_WORD = re.compile(r"[a-z0-9]+")
N_HASH, BANDS = 32, 16


def _shingles(text: str, k: int = 3) -> set[int]:
    w = _WORD.findall(text.lower())
    if len(w) < k:
        return {int(hashlib.md5(" ".join(w).encode()).hexdigest()[:12], 16)}
    return {int(hashlib.md5(" ".join(w[i: i + k]).encode()).hexdigest()[:12], 16) for i in range(len(w) - k + 1)}


def _signature(sh: set[int]) -> tuple[int, ...]:
    return tuple(min((s * (2 * i + 1) + i * 0x9E3779B1) & 0xFFFFFFFFFFFF for s in sh) for i in range(N_HASH))


class Deduper:
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.exact: set[str] = set()
        self.buckets: dict[tuple[int, tuple[int, ...]], list[int]] = {}
        self.sets: list[set[int]] = []

    @staticmethod
    def _norm(text: str) -> str:
        return " ".join(_WORD.findall(text.lower()))

    def add(self, text: str) -> bool:
        """Register ``text``; returns False if it duplicates something already seen."""
        h = hashlib.sha256(self._norm(text).encode()).hexdigest()
        if h in self.exact:
            return False
        sh = _shingles(text)
        sig = _signature(sh)
        rows = N_HASH // BANDS
        keys = [(b, sig[b * rows: (b + 1) * rows]) for b in range(BANDS)]
        for k in keys:
            for j in self.buckets.get(k, ()):
                o = self.sets[j]
                if len(sh & o) / max(1, len(sh | o)) >= self.threshold:
                    return False
        idx = len(self.sets)
        self.sets.append(sh)
        for k in keys:
            self.buckets.setdefault(k, []).append(idx)
        self.exact.add(h)
        return True
