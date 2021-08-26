import requests
from flask import request
from functools import wraps
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs


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
            log.warning(fail_message)
            return {'status': 'fail', 'message':fail_message}, 403

        headers = {
            "Tenantid": headers["Tenantid"],
            "Authorization": headers["Authorization"]
        }

        response = requests.get(url=envs.AUTH_USER_CHECK_URL, headers=headers)
        
        if response.status_code != 200:
            return {'status': 'fail', 'message':fail_message}, 401
        
        return f(*args, **kwargs)
        
    return decorated
