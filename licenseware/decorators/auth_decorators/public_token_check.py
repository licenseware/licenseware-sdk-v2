from flask import request
from functools import wraps
from licenseware.utils.logger import log
from licenseware.common.constants import envs


def public_token_check(f):
    """ Checks if a public token si valid """
    @wraps(f)
    def decorated(*args, **kwargs):

        public_token = request.args.get("public_token")
        headers = dict(request.headers)

        if public_token is None:
            log.warning(f'AUTHORIZATION MISSING  | Request headers: {headers} | URL {request.url}')
            return {"status": "fail", "message": "Query param: `public_token` not provided"}, 403

        # TODO - check token in db

        return f(*args, **kwargs)

    return decorated

