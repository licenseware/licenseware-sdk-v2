# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import pickle
from datetime import timedelta
from typing import Any

from redis import Redis


class RedisCache:
    def __init__(self, config: Config, **kwargs):
        self.redis = Redis(
            host=kwargs.get("host") or config.REDIS_HOST,
            port=kwargs.get("port") or config.REDIS_PORT,
            db=kwargs.get("db") or config.REDIS_RESULT_CACHE_DB,
            password=kwargs.get("password") or config.REDIS_PASSWORD,
        )

    def get(self, match: str):
        stored_keys = []
        cur, keys = self.redis.scan(cursor=0, match=match, count=100)
        stored_keys.extend(keys)
        while cur != 0:
            cur, keys = self.redis.scan(cursor=cur, match=match, count=100)
            stored_keys.extend(keys)
        results = [self.get_key(key) for key in stored_keys]
        return results

    def get_key(self, key: str) -> str:
        return self._deserialize(self.redis.get(key))

    def set(self, key: str, value: Any, expiry: int) -> bool:
        if expiry is not None:
            expiry = timedelta(seconds=expiry)
        return self.redis.set(key, self._serialize(value), ex=expiry)

    def sadd(self, key: str, value: str) -> bool:
        return self.redis.sadd(key, value)

    def smembers(self, key: str) -> set:
        return self._deserialize(self.redis.smembers(key))

    def delete(self, *args) -> bool:
        return self.redis.delete(*args)

    def _serialize(self, obj):
        return pickle.dumps(obj)

    def _deserialize(self, obj):
        if not obj:
            return None
        return pickle.loads(obj)

    def _decode(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return obj
