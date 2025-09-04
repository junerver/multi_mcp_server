import time
from typing import Optional, Dict, Any


# 缓存类
class Cache:
    def __init__(self, ttl: int = 300):  # 默认缓存5分钟
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data = self._cache[key]
            if time.time() - data["timestamp"] < self._ttl:
                return data["value"]
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = {"value": value, "timestamp": time.time()}

    def clear(self) -> None:
        self._cache.clear()
