from functools import wraps

import requests
from flask import request

from licenseware.common.constants import envs
from licenseware.utils.logger import log


def machine_check(f):
    """
    Checks if a machine is authorized
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        if envs.DESKTOP_ENVIRONMENT:
            return f(*args, **kwargs)

        fail_message = "Missing Authorization information"

        headers = dict(request.headers)

        if "Authorization" not in headers:
            log.warning(fail_message)
            return {"status": "fail", "message": fail_message}, 403

        headers = {"Authorization": headers["Authorization"]}
        response = requests.get(url=envs.AUTH_MACHINE_CHECK_URL, headers=headers)

        if response.status_code != 200:
            return {"status": "fail", "message": fail_message}, 401

        return f(*args, **kwargs)

    return decorated
