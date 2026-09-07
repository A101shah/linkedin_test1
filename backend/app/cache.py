import time
from typing import Any

class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self._items: dict[str, tuple[float, Any]] = {}

    def set(self, key: str, value: Any) -> None:
        self._items[key] = (time.time() + self.ttl, value)

    def get(self, key: str) -> Any | None:
        item = self._items.get(key)
        if not item:
            return None
        expires, value = item
        if expires <= time.time():
            self._items.pop(key, None)
            return None
        return value

    def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def clear(self) -> None:
        self._items.clear()
