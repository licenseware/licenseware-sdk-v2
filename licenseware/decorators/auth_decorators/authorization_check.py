from tabnanny import check
from urllib import response
import requests
from flask import request
from functools import wraps
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from cachetools import TTLCache, cached



def authorization_check(f):
    """
        Checks if a user is authorized
    """
    
    @wraps(f)
    def decorated(*args, **kwargs):
        
        fail_message = "Missing Tenant or Authorization information"
        headers = dict(request.headers)
        
        # log.debug(headers.keys())
        #TODO flask or swagger alters headers by adding .capitalize() on them, probably.. 
        
        if "Authorization" not in headers or "Tenantid" not in headers:
            log.warning(f'AUTHORIZATION MISSING  | Request headers: {headers} | URL {request.url}')
            return {'status': 'fail', 'message':fail_message}, 403

        user_authorized = check_authorization((headers['Tenantid'], headers['Authorization']))
        
        if not user_authorized:
            log.warning(f'AUTHORIZATION FAIL | Request headers: {headers} | URL {request.url} | Message: {response.text}')
            return {'status': 'fail', 'message':fail_message}, 401
        
        return f(*args, **kwargs)
        
    return decorated

cache = TTLCache(maxsize=10, ttl=60)


@cached(cache=TTLCache(maxsize=10, ttl=60))
def check_authorization(auth_tuple: tuple):
    headers = {
        "Tenantid": auth_tuple[0],
        "Authorization": auth_tuple[1]
    }

    response = requests.get(url=envs.AUTH_USER_CHECK_URL, headers=headers)
    
    if response.status_code != 200:
        user_authorized = False
    else:
        user_authorized = True
    return user_authorized