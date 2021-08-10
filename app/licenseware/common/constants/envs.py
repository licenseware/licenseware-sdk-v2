"""

Here `envs` is a class which holds environment variables information.

Uppercase attributes are computed at startup and they can't hold dynamic variables
`envs.LWARE_USER` is the value got from os.getenv("LWARE_IDENTITY_USER")


Lowercase attributes are computed on calling them as they are methods
`envs.get_auth_token()`
`get_auth_token` is a class method which is returns a dynamically gathered variable


Make all methods classmethods 
That way we can call them like this `envs.get_auth_token()` instead of this `envs().get_auth_token()`


"""

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

    #Envs available at startup
    LWARE_USER:str = os.getenv("LWARE_IDENTITY_USER")
    LWARE_PASSWORD:str = os.getenv("LWARE_IDENTITY_PASSWORD")
    AUTH_USERS_URL:str = get_auth_users_url()
    AUTH_MACHINES_URL:str = get_auth_machines_url()
    AUTH_BASE_URL:str = os.getenv("AUTH_SERVICE_URL")
    AUTH_MACHINES_ROUTE:str = os.getenv("AUTH_SERVICE_MACHINES_URL_PATH")
    AUTH_USERS_ROUTE:str = os.getenv('AUTH_SERVICE_USERS_URL_PATH')
    
    #Envs added later
    @classmethod
    def get_auth_token(cls):
        return os.getenv('AUTH_TOKEN')
    
    @classmethod
    def get_auth_token_datetime(cls):
        return os.getenv('AUTH_TOKEN_DATETIME')
    
    @classmethod
    def get_tenant_id(cls):
        return os.getenv('TENANT_ID')
    
    @classmethod
    def is_app_authenticated(cls):
        return bool(os.getenv('APP_AUTHENTICATED'))
    
    
