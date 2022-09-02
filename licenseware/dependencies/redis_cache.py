from datetime import timedelta
from typing import List

from redis import Redis

from licenseware.common.constants import envs


class RedisCache:
    def __init__(
        self, host: str = None, port: int = None, db: int = None, password: str = None
    ):
        self.redis = Redis(
            host=host or envs.REDIS_HOST,
            port=port or envs.REDIS_PORT,
            db=db or envs.REDIS_RESULT_CACHE_DB,
            password=password or envs.REDIS_PASSWORD,
        )

    def get(self, key: str) -> str:
        return self.redis.get(key)

    def set(self, key: str, value: bytes, expiry: int) -> bool:
        assert isinstance(value, bytes), "value must be bytes"
        return self.redis.set(key, value, ex=timedelta(seconds=expiry))

    def sadd(self, key: str, value: str) -> bool:
        return self.redis.sadd(key, value)

    def smembers(self, key: str) -> set:
        return self.redis.smembers(key)

    def delete(self, *keys: List[str]) -> bool:
        return self.redis.delete(*keys)
