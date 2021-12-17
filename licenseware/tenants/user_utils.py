import requests
from flask import Request
from licenseware.common.constants import envs
from licenseware.utils.logger import log



def user_is_tenant_owner(flask_request:Request):
    """ Check from the request given if the current user is the tenant owner """
    
    tenant_id  = flask_request.headers.get("TenantId")
    auth_token = flask_request.headers.get("Authorization")
    
    response = requests.get(
        url=envs.AUTH_SERVICE_URL + "/verify-tenant-owner",
        headers={
            "TenantId":  tenant_id,
            "Authorization": auth_token 
        }              
    )
    
    if response.status_code == 200:
        return True
    
    return False




def get_user_profile(flask_request:Request, field:str = None):
    """ Get user profile data from auth from the request given """

    tenant_id  = flask_request.headers.get("TenantId")
    auth_token = flask_request.headers.get("Authorization")
    
    response = requests.get(
        url=envs.AUTH_SERVICE_URL + "/profile",
        headers={
            'TenantId': tenant_id,
            'Authorization': auth_token
        }
    )
    
    if response.status_code != 200:
        log.error(response.content)
        raise Exception(f"Could not get user profile")

    if field:
        return response.json()[field]
        
    return response.json()
    
