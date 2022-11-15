# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

from licenseware.redis_cache.redis_cache import RedisCache


def get_redis_cache(config: Config):
    return RedisCache(config)
