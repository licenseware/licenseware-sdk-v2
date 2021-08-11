'''

Here `envs` is a class which holds environment variables information.

Uppercase attributes are computed at startup and they can't hold dynamic variables
`envs.LWARE_USER` is the value got from os.getenv('LWARE_IDENTITY_USER')


Lowercase attributes are computed on calling them as they are methods
`envs.get_auth_token()`
`get_auth_token` is a class method which is returns a dynamically gathered variable


Make all methods classmethods 
That way we can call them like this `envs.get_auth_token()` instead of this `envs().get_auth_token()`


'''

import os
from dataclasses import dataclass


def get_auth_users_url():
    
    if os.getenv('AUTH_SERVICE_URL') and os.getenv('AUTH_SERVICE_USERS_URL_PATH'):
        return os.getenv('AUTH_SERVICE_URL') + os.getenv('AUTH_SERVICE_USERS_URL_PATH')
    
    return None


def get_auth_machines_url():

    if os.getenv('AUTH_SERVICE_URL') and os.getenv('AUTH_SERVICE_MACHINES_URL_PATH'):
        return os.getenv('AUTH_SERVICE_URL') + os.getenv('AUTH_SERVICE_MACHINES_URL_PATH')
        
    return None


# usually machine name is `name-service` where name is id
_app_id = os.getenv("LWARE_IDENTITY_USER").split('-')[0].upper()


@dataclass
class envs:

    # Environment variables available at startup
    
    APP_ID:str = _app_id
    LWARE_USER:str = os.getenv('LWARE_IDENTITY_USER')
    LWARE_PASSWORD:str = os.getenv('LWARE_IDENTITY_PASSWORD')
    
    AUTH_USERS_URL:str = get_auth_users_url()
    AUTH_MACHINES_URL:str = get_auth_machines_url()
    AUTH_BASE_URL:str = os.getenv('AUTH_SERVICE_URL')
    AUTH_MACHINES_ROUTE:str = os.getenv('AUTH_SERVICE_MACHINES_URL_PATH')
    AUTH_USERS_ROUTE:str = os.getenv('AUTH_SERVICE_USERS_URL_PATH')
    AUTH_MACHINE_CHECK_URL:str = os.getenv('AUTH_SERVICE_URL') + '/machine_authorization'
    AUTH_USER_CHECK_URL:str = os.getenv('AUTH_SERVICE_URL') + '/verify'
    
    REGISTRY_SERVICE_URL:str = os.getenv('REGISTRY_SERVICE_URL')
    REGISTER_APP_URL:str = os.getenv('REGISTRY_SERVICE_URL') + '/apps'
    REGISTER_UPLOADER_URL:str = os.getenv("REGISTRY_SERVICE_URL") + '/uploaders'
    
    BASE_URL:str = os.getenv('API_HOST')
    PORT:str = os.getenv('API_PORT')
    APP_PREFIX:str = os.getenv('APP_URL_PREFIX') or _app_id
    UPLOAD_PATH:str = os.getenv("UPLOAD_PATH", 'tmp/lware')
    
    # Base mongo collection names
    MONGO_DATA_NAME:str = _app_id + "Data"
    MONGO_UTILIZATION_NAME:str = _app_id + "Utilization"
    MONGO_ANALYSIS_NAME:str = _app_id + "Analysis"

    
    # Environment variables added later by the app
    # envs.method_name() - calls the variable dynamically 
    # you can access class vars with cls.attr_name ex: cls.MONGO_ANALYSIS_NAME
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
    def app_is_authenticated(cls):
        return bool(os.getenv('APP_AUTHENTICATED'))
    
    
