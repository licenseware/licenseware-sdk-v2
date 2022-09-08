from contextlib import suppress
from typing import Callable, Dict, List

import flask

from licenseware.common.constants import envs
from licenseware.utils.miscellaneous import get_flask_request_dict


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


def add_app_path_to_broker_funcs(broker_funcs):
    """Add /app-path prefix to given paths"""

    if broker_funcs is None:
        return {}

    broker_funcs_path = {}
    for path, funcli in broker_funcs.items():
        app_path = path if envs.APP_PATH in path else envs.APP_PATH + path
        broker_funcs_path[app_path] = funcli

    return broker_funcs_path


def trigger_broker_funcs(
    flask_request: flask.Request,
    broker_funcs: Dict[str, List[Callable]],
    **extra_params
):
    """

    Parameter `broker_funcs` is available on AppBuilder and UploaderBuilder

    Usage:
    ```py

    App = AppBuilder(
        broker_funcs={"/some-path": [dramatiq_broker_func1, etc]}
    )

    # or

    some_uploader = UploaderBuilder(
        ...
        broker_funcs={
            "/uploads/universal_uploader/files": [dramatiq_broker_func1]
        }
    )


    # Usage in Flask-Restx Resource class

    class ResApi(Resource):
        ...
        def get(self):
            ...
            upload_response = uploader.upload_files(request)
            if uploader.broker_funcs:
                trigger_broker_funcs(request, uploader.broker_funcs, upload_response=upload_response[0])

    ```
    When the path is called the broker functions will be triggered

    """

    broker_funcs = add_app_path_to_broker_funcs(broker_funcs)

    if flask_request.path in broker_funcs:
        flask_request_dict = get_flask_request_dict(flask_request)
        for broker_func in broker_funcs[flask_request.path]:
            broker_func.send({**flask_request_dict, **extra_params})
