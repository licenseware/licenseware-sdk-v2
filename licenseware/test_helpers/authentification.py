import os
import requests
from licenseware.common.constants import envs
from licenseware.utils.logger import log


EMAIL = os.environ['TEST_USER_EMAIL']
PASSWORD = os.environ['TEST_USER_PASSWORD']


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
    
    response = requests.post(envs.AUTH_SERVICE_URL, json=payload)
    
    # log.info(response.content)
    
    return response.json()
    
    

def login_user(email:str, password:str):
    
    response = requests.post(
        envs.AUTH_SERVICE_URL + '/login', 
        json={"email": email, "password": password}
    )
    
    # log.info(response.content)
    
    return response.json()




def get_auth_headers():
    
    # log.info(f"Authentificating with '{EMAIL}'")
    
    login_response = login_user(EMAIL, PASSWORD)
    
    if login_response['status'] == 'success':
        login_response.pop('status')
        login_response.pop('message')        
        # log.info(login_response)
        return login_response
    else:
        create_user(EMAIL, PASSWORD)
        return get_auth_headers()
        
    
    
# auth_headers = get_auth_headers()

# log.warning(auth_headers)