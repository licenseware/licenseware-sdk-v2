import pickle
from functools import wraps
from typing import List, Callable, Dict

from flask import Request

from licenseware.dependencies.redis_cache import RedisCache
from licenseware.utils.common import get_http_request_tenant_id
from licenseware.utils.miscellaneous import serialize_flask_request


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
            _save_key_to_tenant_id(hashed_request)

            return result

        return wrapper

    return decorator(fn) if fn else decorator


def _save_key_to_tenant_id(key: bytes, tenant_id: str = None):
    if tenant_id is None:
        tenant_id = get_http_request_tenant_id()
    if tenant_id is not None:
        caching_database.sadd(tenant_id, key)


def clear_caches_for_tenant_id(tenant_id: str = None):
    if tenant_id is None:
        tenant_id = get_http_request_tenant_id()
    if tenant_id is not None:
        keys = caching_database.smembers(tenant_id)
        caching_database.delete(tenant_id, *keys)


def trigger_broker_funcs(flask_request: Request, broker_funcs: Dict[str, List[Callable]]):
    if flask_request.path in broker_funcs:
        flask_request_dict = serialize_flask_request(flask_request)
        for broker_func in broker_funcs[flask_request.path]:
            broker_func.send(flask_request_dict)