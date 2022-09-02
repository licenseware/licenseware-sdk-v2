from functools import wraps

from flask import request

from licenseware.utils.logger import log
from licenseware.utils.tokens import valid_public_token


def public_token_check(f):
    """Checks if a public token si valid"""

    @wraps(f)
    def decorated(*args, **kwargs):

        public_token = request.args.get("public_token")
        headers = dict(request.headers)

        if public_token is None:
            log.warning(
                f"PUBLIC TOKEN INVALID  | Request headers: {headers} | URL {request.url}"
            )
            return {"status": "fail", "message": "Public token missing or invalid"}, 403

        if not valid_public_token(public_token):
            log.warning(
                f"PUBLIC TOKEN INVALID  | Request headers: {headers} | URL {request.url}"
            )
            return {"status": "fail", "message": "Public token missing or invalid"}, 403

        return f(*args, **kwargs)

    return decorated
