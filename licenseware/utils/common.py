from contextlib import suppress

import flask


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
