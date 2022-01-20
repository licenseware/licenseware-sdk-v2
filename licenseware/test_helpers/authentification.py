import os
import requests
from licenseware.common.constants import envs
from licenseware.utils.logger import log


EMAIL = os.getenv('TEST_USER_EMAIL')
PASSWORD = os.getenv('TEST_USER_PASSWORD')


def get_auth_tables(table:str = None):
    """
        Tables: users, tenants, shared_tenants
        A machine request is used to get the auth tables
    """

    response = requests.get(
        envs.AUTH_SERVICE_URL + '/auth-tables',
        headers={"Authorization": envs.get_auth_token()} 
    )
    
    if table:
        return response.json()[table]

    return response.json()


def get_invite_token(email:str, tenant_id:str):
    """
        Get the invite token for the email and tenant_id provided 
    """

    shared_tenants = get_auth_tables('shared_tenants')

    invite_token = None
    for st in shared_tenants:
        if st['invited_email'] == email and st['tenant_id'] == tenant_id:
            invite_token = st['invite_token']
            break

    assert invite_token

    return invite_token



def create_user(
    email:str, 
    password:str, 
    invited_tenant:str = None,
    first_name:str = None,
    last_name:str = None,
    company_name:str = None,
    job_title:str = None
):

    invite_token = None
    if invited_tenant:
        invite_token = get_invite_token(email, invited_tenant)
    
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name or email.split("@")[0],
        "last_name": last_name or "",
        "company_name": company_name or email.split("@")[1].split('.')[0],
        "job_title": job_title or ""
    }
    
    response = requests.post(
        envs.AUTH_SERVICE_URL, 
        json=payload, 
        params={'invite_token': invite_token} if invite_token is not None else None
    )
    
    # log.info(response.content)
    
    return response.json()
    
    

def login_user(email:str, password:str, invited_tenant:str = None):
    
    invite_token = None
    if invited_tenant:
        invite_token = get_invite_token(email, invited_tenant)
    
    response = requests.post(
        envs.AUTH_SERVICE_URL + '/login', 
        json={"email": email, "password": password},
        params={'invite_token': invite_token} if invite_token is not None else None
    )
    
    return response.json()




def get_auth_headers(email:str = None, password:str = None, invited_tenant:str = None):
    """
        This function creates the user or logs in the user
        If email and password are not provided they will be taken from envs (TEST_USER_EMAIL, TEST_USER_PASSWORD)
        If invited_tenant parameter is provided then the user will be registered/logged with invite token from shared_tenants table
        Returns Authentification headers required to make a request
    """

    # log.info(f"Authentificating with '{EMAIL}'")
    
    login_response = login_user(email or EMAIL, password or PASSWORD, invited_tenant)
    
    if login_response['status'] == 'success':
        login_response.pop('status')
        login_response.pop('message')        
        # log.info(login_response)
        return login_response
    else:
        create_user(email or EMAIL, password or PASSWORD, invited_tenant)
        return get_auth_headers(email, password, invited_tenant)
        
    