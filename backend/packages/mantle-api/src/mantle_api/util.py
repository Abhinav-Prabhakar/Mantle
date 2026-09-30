from __future__ import annotations

import math
import threading
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

import numpy as np


def clean(o: Any) -> Any:
    """Make numpy / NaN values JSON-safe (NaN and inf become null)."""
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return f if math.isfinite(f) else None
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


class LRU:
    """Tiny thread-safe LRU keyed by hashable tuples."""

    def __init__(self, size: int):
        self.size = size
        self.d: OrderedDict[Any, Any] = OrderedDict()
        self.lock = threading.Lock()

    def get_or(self, key: Any, fn: Callable[[], Any]) -> Any:
        with self.lock:
            if key in self.d:
                self.d.move_to_end(key)
                return self.d[key]
        val = fn()
        with self.lock:
            self.d[key] = val
            self.d.move_to_end(key)
            while len(self.d) > self.size:
                self.d.popitem(last=False)
        return val

    def clear(self) -> None:
        with self.lock:
            self.d.clear()
