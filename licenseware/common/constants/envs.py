"""

Here `envs` is a class which holds environment variables information.

Uppercase attributes are computed at startup and they can't hold dynamic variables
`envs.LWARE_USER` is the value got from os.getenv('LWARE_IDENTITY_USER')


Lowercase attributes are computed on calling them as they are methods
`envs.get_auth_token()`
`get_auth_token` is a class method which is returns a dynamically gathered variable


Make all methods classmethods 
That way we can call them like this `envs.get_auth_token()` instead of this `envs().get_auth_token()`


"""

import os
import uuid
from dataclasses import dataclass

from licenseware.common.constants.envs_helpers import (
    get_mongo_connection_string,
    get_upload_path_on_desktop,
)

# Atention!
# > To keep this file short please add only variables used on most/all apps


@dataclass
class envs:

    # Environment variables available at startup
    DESKTOP_ENVIRONMENT: bool = os.getenv("ENVIRONMENT") == "desktop"
    DESKTOP_TENANT_ID: str = str(
        uuid.uuid5(uuid.NAMESPACE_OID, "desktop-user")
    )  # '2655d513-9883-5b7e-8a14-c030bc1ca3b8'
    APP_ID: str = os.getenv("APP_ID", "") if not DESKTOP_ENVIRONMENT else "api"
    APP_NAME: str = os.getenv("APP_NAME")
    LWARE_USER: str = (
        os.getenv("LWARE_IDENTITY_USER", "") if not DESKTOP_ENVIRONMENT else "user"
    )
    LWARE_PASSWORD: str = (
        os.getenv("LWARE_IDENTITY_PASSWORD", "") if not DESKTOP_ENVIRONMENT else "pass"
    )
    DEBUG: bool = os.getenv("DEBUG") == "true"
    ENVIRONMENT: str = (
        os.getenv("ENVIRONMENT", "production") if not DESKTOP_ENVIRONMENT else "desktop"
    )
    USE_BACKGROUND_WORKER: bool = (
        os.getenv("USE_BACKGROUND_WORKER", "true") == "true"
        if not DESKTOP_ENVIRONMENT
        else False
    )

    AUTH_SERVICE_URL: str = (
        os.getenv("AUTH_SERVICE_URL", "")
        if not DESKTOP_ENVIRONMENT
        else "http://localhost:5000/api/auth"
    )
    AUTH_MACHINES_URL: str = AUTH_SERVICE_URL + "/machines"
    AUTH_MACHINE_CHECK_URL: str = AUTH_SERVICE_URL + "/machine_authorization"
    AUTH_USER_CHECK_URL: str = AUTH_SERVICE_URL + "/verify"
    AUTH_TENANTS_URL: str = AUTH_SERVICE_URL + "/tenants"
    AUTH_USER_PROFILE_URL: str = AUTH_SERVICE_URL + "/profile"
    AUTH_USER_TABLES_URL: str = AUTH_SERVICE_URL + "/users/tables"

    REGISTRY_SERVICE_URL: str = (
        os.getenv("REGISTRY_SERVICE_URL", "")
        if not DESKTOP_ENVIRONMENT
        else "http://localhost:5000/api/registry-service"
    )
    REGISTER_ALL_URL: str = REGISTRY_SERVICE_URL + "/v1" + "/registrations"
    REGISTER_APP_URL: str = REGISTRY_SERVICE_URL + "/v1" + "/apps"
    REGISTER_UPLOADER_URL: str = REGISTRY_SERVICE_URL + "/v1" + "/uploaders"
    GET_UPLOADERS_URL: str = REGISTRY_SERVICE_URL + "/uploaders"
    REGISTER_UPLOADER_STATUS_URL: str = (
        REGISTRY_SERVICE_URL + "/v1" + "/uploaders/status"
    )
    REGISTER_REPORT_URL: str = REGISTRY_SERVICE_URL + "/v1" + "/reports"
    REGISTER_REPORT_COMPONENT_URL: str = REGISTER_REPORT_URL + "/v1" + "/components"

    APP_HOST: str = (
        os.getenv("APP_HOST", "")
        if not DESKTOP_ENVIRONMENT
        else "http://localhost:5000"
    )
    QUEUE_NAME: str = os.getenv("QUEUE_NAME", APP_ID.replace("-service", ""))
    APP_PATH: str = os.getenv("APP_PATH", "/" + QUEUE_NAME)
    BASE_URL: str = os.getenv("BASE_URL", APP_HOST + APP_PATH)
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")
    SECRET: str = os.getenv("SECRET", LWARE_PASSWORD)

    UPLOAD_PATH: str = "/uploads"
    REPORT_PATH: str = "/reports"
    FEATURE_PATH: str = "/features"
    DATA_SYNC_PATH: str = "/datasync"
    REPORT_COMPONENT_PATH: str = "/report-components"
    UPLOAD_URL: str = BASE_URL + UPLOAD_PATH
    REPORT_URL: str = BASE_URL + REPORT_PATH
    FEATURES_URL: str = BASE_URL + FEATURE_PATH
    REPORT_COMPONENT_URL: str = BASE_URL + REPORT_COMPONENT_PATH
    FILE_UPLOAD_PATH: str = (
        os.getenv("FILE_UPLOAD_PATH", "tmp/lware")
        if not DESKTOP_ENVIRONMENT
        else get_upload_path_on_desktop()
    )
    DEPLOYMENT_SUFFIX: str = os.getenv("DEPLOYMENT_SUFFIX")

    # Mongo connection
    MONGO_DATABASE_NAME: str = (
        os.getenv("MONGO_DATABASE_NAME") or os.getenv("MONGO_DB_NAME") or "db"
    )
    MONGO_CONNECTION_STRING: str = (
        os.getenv("MONGO_CONNECTION_STRING") or get_mongo_connection_string()
    )

    # !!! Add here ONLY collection names that are USED on ALL or MOST of the APPS !!!
    # For APP SPECIFIC mongo collection names you can always create a data class in `common`/`utils` or other app package.
    # Another solution would be to extend this class and import it from the file you are extending it.
    COLLECTION_PREFIX = os.getenv("COLLECTION_PREFIX", QUEUE_NAME.upper())
    MONGO_COLLECTION_DATA_NAME: str = COLLECTION_PREFIX + "Data"
    MONGO_COLLECTION_UTILIZATION_NAME: str = COLLECTION_PREFIX + "Quota"
    MONGO_COLLECTION_ANALYSIS_NAME: str = (
        COLLECTION_PREFIX + "History"
    )  # Depreciated use MONGO_COLLECTION_HISTORY_NAME instead
    MONGO_COLLECTION_HISTORY_NAME: str = COLLECTION_PREFIX + "ProcessingHistory"
    MONGO_COLLECTION_UPLOADERS_STATUS_NAME: str = COLLECTION_PREFIX + "UploadersStatus"
    MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME: str = (
        COLLECTION_PREFIX + "ReportSnapshots"
    )  #! OUTDATED NEEDS PAGINATION
    MONGO_COLLECTION_FEATURES_NAME: str = COLLECTION_PREFIX + "Features"
    MONGO_COLLECTION_TOKEN_NAME: str = COLLECTION_PREFIX + "Tokens"

    # Redis connection
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    REDIS_RESULT_CACHE_DB: int = int(os.getenv("REDIS_RESULT_CACHE_DB", "15"))

    DEAD_MESSAGE_TTL: int = int(os.getenv("DEAD_MESSAGE_TTL", "3600"))

    PROMETHEUS_ENABLED: bool = os.getenv("PROMETHEUS_ENABLED", "").lower() == "true"
    METRICS_URI: str = os.getenv("METRICS_URI", "/metrics")

    # Environment variables added later by the app
    # envs.method_name() - calls the variable dynamically
    # you can access class vars with cls.attr_name ex: cls.MONGO_COLLECTION_DATA_NAME
    @classmethod
    def get_auth_token(cls):
        return os.getenv("AUTH_TOKEN")

    @classmethod
    def get_auth_token_datetime(cls):
        return os.getenv("AUTH_TOKEN_DATETIME")

    @classmethod
    def app_is_authenticated(cls):
        return os.getenv("APP_AUTHENTICATED") == "true"

    @classmethod
    def environment_is_local(cls):
        return os.getenv("ENVIRONMENT") == "local"

    @classmethod
    def get_tenant_upload_path(cls, tenant_id: str):
        DESKTOP_ENVIRONMENT = os.getenv("ENVIRONMENT") == "desktop"
        FILE_UPLOAD_PATH = (
            os.getenv("FILE_UPLOAD_PATH", "tmp/lware")
            if not DESKTOP_ENVIRONMENT
            else get_upload_path_on_desktop()
        )
        return os.path.join(FILE_UPLOAD_PATH, tenant_id)
