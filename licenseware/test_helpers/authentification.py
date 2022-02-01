import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine



def get_auth_tables(auth_headers:dict, table:str = None):
    """
        Tables: users, tenants, shared_tenants
        A machine request is used to get the auth tables
    """

    response = requests.get(
        envs.AUTH_SERVICE_URL + '/users/tables',
        headers=auth_headers
    )

    # log.debug(auth_headers)
    # log.debug(response.content)
    
    if table:
        return response.json()[table]

    return response.json()


def get_invite_token(email, invited_tenant, auth_headers):
    """
        Get the invite token for the email and tenant_id provided 
    """

    shared_tenants = get_auth_tables(auth_headers, 'shared_tenants')

    invite_token = None
    for st in shared_tenants:
        if st['invited_email'] == email and st['tenant_id'] == invited_tenant:
            invite_token = st['invite_token']
            break

    assert invite_token

    return invite_token



def login_user_with_invite_token(email, password, invited_tenant, auth_headers):

    invite_token = get_invite_token(email, invited_tenant, auth_headers)

    response = requests.post(
        envs.AUTH_SERVICE_URL + '/login', 
        json={"email": email, "password": password},
        params={'invite_token': invite_token}
    )
    
    # log.debug(response.content)

    return response.json()



def create_user(
    email:str, 
    password:str, 
    first_name:str = None,
    last_name:str = None,
    company_name:str = None,
    job_title:str = None
):
    
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name or email.split("@")[0],
        "last_name": last_name or "",
        "company_name": company_name or email.split("@")[1].split('.')[0],
        "job_title": job_title or ""
    }
    
    response = requests.post(
        envs.AUTH_SERVICE_URL + '/users/register', 
        json=payload
    )

    # log.debug(response)

    return response.json()

    
    
def login_user(email:str, password:str):
    

    response = requests.post(
        envs.AUTH_SERVICE_URL + '/login', 
        json={"email": email, "password": password}
    )

    # log.debug(response.content)

    return response.json()




@authenticated_machine
def get_auth_headers(email:str, password:str, invited_tenant:str = None):
    """
        This function creates the user or logs in the user
        If invited_tenant parameter is provided then the user will be registered/logged with invite token from shared_tenants table
        Returns Authentification headers required to make a request
    """

    # log.debug(f"> get_auth_headers: {email} {password}, {invited_tenant}")

    login_response = login_user(email, password)
    
    if login_response['status'] == 'success':
        login_response.pop('status')
        login_response.pop('message')        
        return login_response
    else:
        
        create_user(email, password)

        if invited_tenant is not None:
            response = login_user(email, password)
            assert response['status'] == 'success'
            return login_user_with_invite_token(email, password, invited_tenant, auth_headers=response)

        return get_auth_headers(email, password, invited_tenant)
        