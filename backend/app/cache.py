import json
import time
from typing import Any
from redis.asyncio import Redis

class TTLCache:
    def __init__(self, ttl_seconds: int, redis_url: str | None = None):
        self.ttl = ttl_seconds
        self._items: dict[str, tuple[float, Any]] = {}
        self.redis = Redis.from_url(redis_url, decode_responses=True) if redis_url else None

    async def set(self, key: str, value: Any) -> None:
        if self.redis:
            await self.redis.set(key, json.dumps(value), ex=self.ttl)
        else:
            self._items[key] = (time.time() + self.ttl, value)

    async def get(self, key: str) -> Any | None:
        if self.redis:
            raw = await self.redis.get(key)
            return json.loads(raw) if raw else None
        item = self._items.get(key)
        if not item:
            return None
        expires, value = item
        if expires <= time.time():
            self._items.pop(key, None)
            return None
        return value

    async def delete(self, key: str) -> None:
        if self.redis:
            await self.redis.delete(key)
        else:
            self._items.pop(key, None)
