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



@dataclass
class envs:

    # Environment variables available at startup
    APP_ID:str = os.environ["APP_ID"]
    LWARE_USER:str = os.environ['LWARE_IDENTITY_USER']
    LWARE_PASSWORD:str = os.environ['LWARE_IDENTITY_PASSWORD']
    PERSONAL_SUFFIX:str = os.getenv("PERSONAL_SUFFIX", "")
    ENVIRONMENT:str = os.getenv("ENVIRONMENT", 'production')
    DEBUG:bool = os.getenv('DEBUG') == 'true'
    USE_BACKGROUND_WORKER:bool = os.getenv('USE_BACKGROUND_WORKER', 'true') == 'true'
    
    AUTH_SERVICE_URL:str = os.environ['AUTH_SERVICE_URL']
    AUTH_MACHINES_URL:str = AUTH_SERVICE_URL + '/machines'
    AUTH_MACHINE_CHECK_URL:str = AUTH_SERVICE_URL + '/machine_authorization'
    AUTH_TENANTS_URL:str = AUTH_SERVICE_URL + '/tenants'
    AUTH_USER_PROFILE_URL:str = AUTH_SERVICE_URL + '/profile'
    

    REGISTRY_SERVICE_URL:str = os.environ['REGISTRY_SERVICE_URL']
    REGISTER_APP_URL:str = REGISTRY_SERVICE_URL + '/apps'
    REGISTER_UPLOADER_URL:str = REGISTRY_SERVICE_URL + '/uploaders'
    REGISTER_UPLOADER_STATUS_URL:str = REGISTRY_SERVICE_URL + '/uploaders/status'
    REGISTER_REPORT_URL:str = REGISTRY_SERVICE_URL + '/reports'
    REGISTER_REPORT_COMPONENT_URL:str = REGISTER_REPORT_URL + '/components'
    
    APP_HOST:str = os.environ['APP_HOST']
    QUEUE_NAME:str = APP_ID if '-service' not in APP_ID else APP_ID.replace('-service', '') #ifmp-service => ifmp
    APP_PATH:str = "/" + QUEUE_NAME
    BASE_URL:str = APP_HOST + APP_PATH
    UPLOAD_PATH:str = '/uploads'
    REPORT_PATH:str = '/reports'
    REPORT_COMPONENT_PATH:str = '/report-components'
    UPLOAD_URL:str = BASE_URL + UPLOAD_PATH
    REPORT_URL:str = BASE_URL + REPORT_PATH
    REPORT_COMPONENT_URL:str = BASE_URL + REPORT_COMPONENT_PATH
    FILE_UPLOAD_PATH:str = os.getenv("FILE_UPLOAD_PATH", 'tmp/lware')
    
    # Mongo connection
    MONGO_DATABASE_NAME:str = os.getenv("MONGO_DATABASE_NAME") or os.getenv("MONGO_DB_NAME") or 'db'
    MONGO_CONNECTION_STRING:str = os.getenv('MONGO_CONNECTION_STRING') or 'mongodb://localhost:27017/db'
    
    # Base mongo collection names
    COLLECTION_PREFIX = APP_ID.replace('-service', '').upper()
    MONGO_COLLECTION_DATA_NAME:str = COLLECTION_PREFIX + "Data"
    MONGO_COLLECTION_UTILIZATION_NAME:str = COLLECTION_PREFIX + "Quota"
    MONGO_COLLECTION_ANALYSIS_NAME:str = COLLECTION_PREFIX + "History"
    
        
    # Environment variables added later by the app
    # envs.method_name() - calls the variable dynamically 
    # you can access class vars with cls.attr_name ex: cls.MONGO_COLLECTION_DATA_NAME
    @classmethod
    def get_auth_token(cls):
        return os.getenv('AUTH_TOKEN')
    
    @classmethod
    def get_auth_token_datetime(cls):
        return os.getenv('AUTH_TOKEN_DATETIME')
    
    @classmethod
    def app_is_authenticated(cls):
        return os.getenv('APP_AUTHENTICATED') == 'true'
            
    @classmethod
    def environment_is_local(cls):
        return os.getenv('ENVIRONMENT') == 'local'
    
    @classmethod
    def get_tenant_upload_path(cls, tenant_id:str):
        return os.path.join(os.getenv("FILE_UPLOAD_PATH", 'tmp/lware'), tenant_id)
    
        
    
