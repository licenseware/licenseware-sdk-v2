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
    
    if os.environ['AUTH_SERVICE_URL'] and os.environ['AUTH_SERVICE_USERS_URL_PATH']:
        return os.environ['AUTH_SERVICE_URL'] + os.environ['AUTH_SERVICE_USERS_URL_PATH']
    
    return None


def get_auth_machines_url():

    if os.environ['AUTH_SERVICE_URL'] and os.environ['AUTH_SERVICE_MACHINES_URL_PATH']:
        return os.environ['AUTH_SERVICE_URL'] + os.environ['AUTH_SERVICE_MACHINES_URL_PATH']
        
    return None



@dataclass
class envs:

    # Environment variables available at startup
    DEBUG:bool = os.environ['DEBUG'] == 'true'
    ENVIRONMENT:str = os.environ["ENVIRONMENT"]
    PERSONAL_PREFIX:str = os.environ["PERSONAL_PREFIX"]
    APP_ID:str = os.environ["APP_ID"]
    APP_HOST:str = os.environ['APP_HOST']
    LWARE_USER:str = os.environ['LWARE_IDENTITY_USER']
    LWARE_PASSWORD:str = os.environ['LWARE_IDENTITY_PASSWORD']
    
    AUTH_USERS_URL:str = get_auth_users_url()
    AUTH_MACHINES_URL:str = get_auth_machines_url()
    AUTH_BASE_URL:str = os.environ['AUTH_SERVICE_URL']
    AUTH_MACHINES_ROUTE:str = os.environ['AUTH_SERVICE_MACHINES_URL_PATH']
    AUTH_USERS_ROUTE:str = os.environ['AUTH_SERVICE_USERS_URL_PATH']
    AUTH_MACHINE_CHECK_URL:str = os.environ['AUTH_SERVICE_URL'] + '/machine_authorization'
    AUTH_USER_CHECK_URL:str = os.environ['AUTH_SERVICE_URL'] + '/verify'
    
    REGISTRY_SERVICE_URL:str = os.environ['REGISTRY_SERVICE_URL']
    REGISTER_APP_URL:str = REGISTRY_SERVICE_URL + '/apps'
    REGISTER_UPLOADER_URL:str = REGISTRY_SERVICE_URL + '/uploaders'
    REGISTER_UPLOADER_STATUS_URL:str = REGISTRY_SERVICE_URL + '/uploaders/status'
    REGISTER_REPORT_URL:str = REGISTRY_SERVICE_URL + '/reports'
    REGISTER_REPORT_COMPONENT_URL:str = REGISTER_REPORT_URL + '/components'
    
    BASE_URL:str = APP_HOST + "/" + APP_ID
    UPLOAD_PATH:str = '/uploads'
    REPORT_PATH:str = '/reports'
    REPORT_COMPONENT_PATH:str = '/report_components'
    UPLOAD_URL:str = BASE_URL + UPLOAD_PATH
    REPORT_URL:str = BASE_URL + REPORT_PATH
    REPORT_COMPONENT_URL:str = BASE_URL + REPORT_COMPONENT_PATH
    FILE_UPLOAD_PATH:str = os.getenv("FILE_UPLOAD_PATH", 'tmp/lware')
    
    # Base mongo collection names
    MONGO_COLLECTION_DATA_NAME:str = os.environ["APP_ID"].upper() + "Data" 
    MONGO_COLLECTION_UTILIZATION_NAME:str = os.environ["APP_ID"].upper() + "Utilization"
    MONGO_COLLECTION_ANALYSIS_NAME:str = os.environ["APP_ID"].upper() + "Analysis"
    
    # Mongo connection data
    MONGO_ROOT_USERNAME:str = os.environ["MONGO_ROOT_USERNAME"]
    MONGO_ROOT_PASSWORD:str = os.environ["MONGO_ROOT_PASSWORD"]
    MONGO_DATABASE_NAME:str = os.environ["MONGO_DATABASE_NAME"]
    MONGO_HOSTNAME:str = os.environ["MONGO_HOSTNAME"]
    MONGO_PORT:str = os.environ["MONGO_PORT"] 
    MONGO_CONNECTION_STRING:str = os.environ['MONGO_CONNECTION_STRING']

    
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
    def app_is_authenticated(cls):
        if os.getenv('APP_AUTHENTICATED') == 'true':
            return True
        return False
        
    
