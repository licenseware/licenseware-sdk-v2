import pickle
from functools import wraps
from typing import Callable

from licenseware.dependencies.redis_cache import RedisCache

caching_database = RedisCache()
TEN_MINUTES = 600


def _serialize(obj):
    return pickle.dumps(obj)


def _deserialize(obj):
    return pickle.loads(obj)


def _hash_args(*args, **kwargs):
    return _serialize((args, kwargs))


def _lookup_value(key):
    value = caching_database.get(key)
    if value:
        return _deserialize(value)


def _save_result(key, result, expiry):
    return caching_database.set(key, _serialize(result), expiry)


def cache_result(fn: Callable = None, expiry: int = TEN_MINUTES) -> Callable:
    """
    Decorator to cache the result of a flask request.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Callable:
            hashed_request = _hash_args(*args, **kwargs)
            cached_result = _lookup_value(hashed_request)

            if cached_result:
                return cached_result

            result = fn(*args, **kwargs)

            _save_result(hashed_request, result, expiry)

            return result

        return wrapper

    return decorator(fn) if fn else decorator
