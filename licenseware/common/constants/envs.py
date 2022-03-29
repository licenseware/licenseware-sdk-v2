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


# Atention! 
# > To keep this file short please add only variables used on most/all apps 

@dataclass
class envs:

    # Environment variables available at startup
    APP_ID:str = os.environ["APP_ID"]
    LWARE_USER:str = os.environ['LWARE_IDENTITY_USER']
    LWARE_PASSWORD:str = os.environ['LWARE_IDENTITY_PASSWORD']
    ENVIRONMENT:str = os.getenv("ENVIRONMENT", 'production')
    DEBUG:bool = os.getenv('DEBUG') == 'true'
    USE_BACKGROUND_WORKER:bool = os.getenv('USE_BACKGROUND_WORKER', 'true') == 'true'
    
    AUTH_SERVICE_URL:str = os.environ['AUTH_SERVICE_URL']
    AUTH_MACHINES_URL:str = AUTH_SERVICE_URL + '/machines'
    AUTH_MACHINE_CHECK_URL:str = AUTH_SERVICE_URL + '/machine_authorization'
    AUTH_USER_CHECK_URL:str = AUTH_SERVICE_URL + '/verify'
    AUTH_TENANTS_URL:str = AUTH_SERVICE_URL + '/tenants'
    AUTH_USER_PROFILE_URL:str = AUTH_SERVICE_URL + '/profile'
    AUTH_USER_TABLES_URL:str = AUTH_SERVICE_URL + '/users/tables'

    REGISTRY_SERVICE_URL:str = os.environ['REGISTRY_SERVICE_URL']
    REGISTER_ALL_URL:str = REGISTRY_SERVICE_URL + '/v1' + '/registrations'
    REGISTER_APP_URL:str = REGISTRY_SERVICE_URL + '/v1' + '/apps'
    REGISTER_UPLOADER_URL:str = REGISTRY_SERVICE_URL + '/v1' + '/uploaders'
    GET_UPLOADERS_URL:str = REGISTRY_SERVICE_URL + '/uploaders'
    REGISTER_UPLOADER_STATUS_URL:str = REGISTRY_SERVICE_URL + '/v1' + '/uploaders/status'
    REGISTER_REPORT_URL:str = REGISTRY_SERVICE_URL + '/v1' + '/reports'
    REGISTER_REPORT_COMPONENT_URL:str = REGISTER_REPORT_URL + '/v1' + '/components'
    

    # NEW -service is NOT removed from appid
    # APP_HOST:str = os.environ['APP_HOST']
    # QUEUE_NAME:str = APP_ID
    # APP_PATH:str = "/" + APP_ID
    # BASE_URL:str = APP_HOST + APP_PATH

    # OLD -service is removed from appid 
    # DEPRECIATED - keep NEW after testing
    APP_HOST:str = os.environ['APP_HOST']
    QUEUE_NAME:str = APP_ID if '-service' not in APP_ID else APP_ID.replace('-service', '') #ifmp-service => ifmp
    APP_PATH:str = "/" + QUEUE_NAME
    BASE_URL:str = APP_HOST + APP_PATH

    UPLOAD_PATH:str = '/uploads'
    REPORT_PATH:str = '/reports'
    FEATURE_PATH:str = '/features'
    REPORT_COMPONENT_PATH:str = '/report-components'
    UPLOAD_URL:str = BASE_URL + UPLOAD_PATH
    REPORT_URL:str = BASE_URL + REPORT_PATH
    FEATURES_URL:str = BASE_URL + FEATURE_PATH
    REPORT_COMPONENT_URL:str = BASE_URL + REPORT_COMPONENT_PATH
    FILE_UPLOAD_PATH:str = os.getenv("FILE_UPLOAD_PATH", 'tmp/lware')
    DEPLOYMENT_SUFFIX:str = os.getenv("DEPLOYMENT_SUFFIX")
    
    
    # Mongo connection
    MONGO_DATABASE_NAME:str = os.getenv("MONGO_DATABASE_NAME") or os.getenv("MONGO_DB_NAME") or 'db'
    MONGO_CONNECTION_STRING:str = os.getenv('MONGO_CONNECTION_STRING') or 'mongodb://localhost:27017/db'
    
    # !!! Add here ONLY collection names that are USED on ALL or MOST of the APPS !!!
    # For APP SPECIFIC mongo collection names you can always create a data class in `common`/`utils` or other app package.
    # Another solution would be to extend this class and import it from the file you are extending it.
    COLLECTION_PREFIX = os.getenv("COLLECTION_PREFIX", QUEUE_NAME.upper())
    MONGO_COLLECTION_DATA_NAME:str = COLLECTION_PREFIX + "Data"
    MONGO_COLLECTION_UTILIZATION_NAME: str = COLLECTION_PREFIX + "Quota"
    MONGO_COLLECTION_ANALYSIS_NAME: str = COLLECTION_PREFIX + "History"  # Depreciated use MONGO_COLLECTION_HISTORY_NAME instead
    MONGO_COLLECTION_HISTORY_NAME: str = COLLECTION_PREFIX + "ProcessingHistory"
    MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME: str = COLLECTION_PREFIX + "ReportSnapshots"
    MONGO_COLLECTION_FEATURES_NAME: str = COLLECTION_PREFIX + "Features"
    
    
        
    # Redis connection
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    REDIS_RESULT_CACHE_DB: int = int(os.getenv("REDIS_RESULT_CACHE_DB", "15"))

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
    
        
    
