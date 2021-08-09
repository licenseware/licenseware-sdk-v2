import os
from dataclasses import dataclass

def get_auth_users_url():
    
    if os.getenv("AUTH_SERVICE_URL") and os.getenv('AUTH_SERVICE_USERS_URL_PATH'):
        return os.getenv("AUTH_SERVICE_URL") + os.getenv('AUTH_SERVICE_USERS_URL_PATH')
    
    return None


def get_auth_machines_url():

    if os.getenv("AUTH_SERVICE_URL") and os.getenv('AUTH_SERVICE_MACHINES_URL_PATH'):
        return os.getenv("AUTH_SERVICE_URL") + os.getenv('AUTH_SERVICE_MACHINES_URL_PATH')
        
    return None


@dataclass
class envs:

    LWARE_USER:str = os.getenv("LWARE_IDENTITY_USER")
    LWARE_PASSWORD:str = os.getenv("LWARE_IDENTITY_PASSWORD")
    AUTH_USERS_URL:str = get_auth_users_url()
    AUTH_MACHINES_URL:str = get_auth_machines_url()
    AUTH_BASE_URL:str = os.getenv("AUTH_SERVICE_URL")
    AUTH_MACHINES_ROUTE:str = os.getenv("AUTH_SERVICE_MACHINES_URL_PATH")
    AUTH_USERS_ROUTE:str = os.getenv('AUTH_SERVICE_USERS_URL_PATH')
    AUTH_TOKEN:str = os.getenv('AUTH_TOKEN')
    TENANT_ID:str = os.getenv('TENANT_ID')
    APP_AUTHENTICATED:bool = bool(os.getenv('APP_AUTHENTICATED'))
    AUTH_TOKEN_DATETIME:str = os.getenv('AUTH_TOKEN_DATETIME')
    