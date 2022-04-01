import flask
from contextlib import suppress
from typing import List, Callable, Dict
from .miscellaneous import get_flask_request_dict


def get_flask_request():
    """
    Get the flask request object.
    """
    with suppress(RuntimeError):
        return flask.request


def get_http_request_tenant_id(flask_request=None):
    """
    Get the tenant id from the request headers.
    """
    if flask_request is None:
        flask_request = get_flask_request()
    if flask_request is not None:
        # TODO: maybe adding `Tenantid`?
        return flask_request.headers.get("TenantId")


def trigger_broker_funcs(
    flask_request: flask.Request, broker_funcs: Dict[str, List[Callable]]
):
    """

    Usage:
    ```py
    App = AppBuilder(
        broker_funcs={"/some-path": [dramatiq_broker_func1, etc]}
    )

    ```
    When the path is called the broker functions will be triggered

    """
    if flask_request.path in broker_funcs:
        flask_request_dict = get_flask_request_dict(flask_request)
        for broker_func in broker_funcs[flask_request.path]:
            broker_func.send(flask_request_dict)
