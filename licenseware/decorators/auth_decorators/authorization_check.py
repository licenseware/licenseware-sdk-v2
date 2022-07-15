import requests
from requests import Response
from flask import request
from functools import wraps
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from cachetools import TTLCache, cached


@cached(cache=TTLCache(maxsize=10, ttl=60))
def _cached_auth_check(tenant_id: str, auth_token: str) -> Response:
    response = requests.get(
        url=envs.AUTH_USER_CHECK_URL,
        headers={
            "Tenantid": tenant_id,
            "Authorization": auth_token
        }
    )
    return response


@cached(cache=TTLCache(maxsize=10, ttl=60))
def _cached_machine_check(auth_token: str) -> Response:

    response = requests.get(
        url=envs.AUTH_MACHINE_CHECK_URL,
        headers={"Authorization": auth_token}
    )

    return response.status_code == 200




def authorization_check(f):
    """ Checks if a user is authorized """
    @wraps(f)
    def decorated(*args, **kwargs):

        if envs.DESKTOP_ENVIRONMENT: return f(*args, **kwargs)

        fail_message = "Missing Tenant or Authorization information"
        headers = dict(request.headers)
        # log.debug(headers.keys())
        # TODO flask or swagger alters headers by adding .capitalize() on them, probably..

        if "Authorization" not in headers or "Tenantid" not in headers:
            log.warning(f'AUTHORIZATION MISSING  | Request headers: {headers} | URL {request.url}')
            return {'status': 'fail', 'message': fail_message}, 403

        response = _cached_auth_check(tenant_id=headers['Tenantid'], auth_token=headers['Authorization'])

        if response.status_code != 200:
            machine_response = False
            reports_paths = request.path.startswith((f"/{envs.APP_PATH}/reports", f"/{envs.APP_PATH}/report-components", ))
            if reports_paths and request.method in ["GET", "POST"]: 
                machine_response = _cached_machine_check(auth_token=headers['Authorization'])

            if machine_response is True:
                log.info("Using `Authorization` for machines on this request")
            else:
                log.warning(f'AUTHORIZATION FAIL | Request headers: {headers} | URL {request.url} | Message: {response.text}')
                return {'status': 'fail', 'message': fail_message}, 401

        return f(*args, **kwargs)

    return decorated

