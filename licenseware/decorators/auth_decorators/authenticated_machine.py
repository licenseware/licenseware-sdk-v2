from functools import wraps

from licenseware.auth import Authenticator
from licenseware.common.constants import envs
from licenseware.utils.logger import log


def authenticated_machine(f):
    """
    Refreshes the authentication token before making a request
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        if envs.DESKTOP_ENVIRONMENT:
            return f(*args, **kwargs)

        response, status_code = Authenticator.connect()
        if status_code not in {200, 201}:
            log.warning("Could not refresh token")
            return {"status": "fail", "message": "Could not refresh token"}, 403

        return f(*args, **kwargs)

    return decorated
