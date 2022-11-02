from licenseware.constants.base_enum import BaseEnum
from licenseware.dependencies import BaseSettings


class Collections(BaseEnum):
    DATA = "Data"
    QUOTA = "Quota"
    HISTORY = "ProcessingHistory"
    REPORT_SNAPSHOTS = "ReportSnapshots"
    FEATURE = "Features"
    TOKEN = "Tokens"
    # Outdated
    MONGO_COLLECTION_ANALYSIS_NAME = "History"


class LogLevel(BaseEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(BaseEnum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"
    DESKTOP = "DESKTOP"


class CeleryBrokerType(BaseEnum):
    REDIS = "REDIS"
    RABBITMQ = "RABBITMQ"


class WebAppFramework(BaseEnum):
    FASTAPI = "FASTAPI"
    FLASK = "FLASK"


class Config(BaseSettings):  # pragma no cover
    APP_ID: str
    APP_SECRET: str
    FILE_UPLOAD_PATH: str = "/tmp/lware"
    CURRENT_ENVIRONMENT: Environment = Environment.DEV
    ENVIRONMENTS: Environment = Environment
    LOG_LEVEL: LogLevel = LogLevel.INFO
    PORT: int = 8000
    DASHBOARD_WORKERS_HOST: str = None
    DASHBOARD_WORKERS_PORT: int = None

    BASE_URL: str

    @property
    def APP_URL(self):
        return self.BASE_URL + "/" + self.APP_ID

    PUBLIC_TOKEN_REPORT_URL: str
    FRONTEND_URL: str

    MACHINE_NAME: str
    MACHINE_PASSWORD: str

    AUTH_SERVICE_URL: str
    AUTH_MACHINE_LOGIN_URL: str
    AUTH_USER_LOGIN_URL: str
    AUTH_USER_INFO_URL: str
    AUTH_MACHINE_CHECK_URL: str
    AUTH_USER_CHECK_URL: str

    REGISTRY_SERVICE_URL: str
    REGISTRY_SERVICE_APPS_URL: str
    REGISTRY_SERVICE_UPLOADERS_URL: str
    REGISTRY_SERVICE_REPORTS_URL: str
    REGISTRY_SERVICE_COMPONENTS_URL: str

    MONGO_HOST: str
    MONGO_DBNAME: str
    MONGO_PORT: int = 27017

    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_COLLECTION: Collections = Collections

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_RESULT_CACHE_DB: int = 1
    REDIS_PASSWORD: str = None
    EXPIRE_REGISTRATION: int = 900  # 15 mins
    EXPIRE_UPLOADER_STATUS: int = 7200  # 2 hours
    EXPIRE_USER_CHECK: int = 60  # 1 minute
    EXPIRE_MACHINE_CHECK: int = 60  # 1 minute
    EXPIRE_NOTIFICATION: int = 259_200  # 3 days

    KAFKA_BROKER_URL: str
    KAFKA_CONSUMER_POLL: float = 1.0
    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"

    JAEGER_MODE: str = "grpc"
    JAEGER_COLLECTOR_ENDPOINT_GRPC_ENDPOINT: str = "jaeger-collector:14250"
    JAEGER_COLLECTOR_THRIFT_URL: str = "http://jaeger-collector:14268"
    JAEGER_AGENT_HOST_NAME: str = "jaeger-agent"
    JAEGER_AGENT_PORT: int = 6831
    OPEN_TELEMETRY_HOST: str = "127.0.0.1"
    OPEN_TELEMETRY_PORT: int = 6831

    CELERY_BROKER_REDIS_DB: int = 1
    CELERY_BACKEND_REDIS_DB: int = 2
    CELERY_BEATS_REGISTRATION_INTERVAL: int = 600  # 10 minutes
    REFRESH_MACHINE_TOKEN_INTERVAL: int = 86_400  # 24 hours

    CELERY_BROKER_TYPE: CeleryBrokerType = CeleryBrokerType.REDIS
    WEBAPP_FRAMEWORK: WebAppFramework = WebAppFramework.FASTAPI

    @property
    def celery_broker_uri(self):
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BROKER_REDIS_DB}"
        )

    @property
    def celery_result_backend_uri(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BACKEND_REDIS_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True
