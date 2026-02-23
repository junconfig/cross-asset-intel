from __future__ import annotations

import time
from typing import Any, Dict, Tuple


class SimpleCache:
    """
    Very simple in-memory cache.
    Stores values for X seconds (TTL = time-to-live).
    """

    def __init__(self) -> None:
        self._store: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        item = self._store.get(key)
        if not item:
            return None

        expires_at, value = item
        if time.time() > expires_at:
            # expired
            self._store.pop(key, None)
            return None

        return value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        expires_at = time.time() + ttl_seconds
        self._store[key] = (expires_at, value)