from dataclasses import asdict, dataclass


@dataclass
class TopicType:

    USER_EVENTS: str = "user_events"
    APP_EVENTS: str = "app_events"
    LOG_EVENTS: str = "log_events"
    DATA_STREAM: str = "data_stream"

    def dict(self):
        return asdict(self)


@dataclass
class EventType:

    ACCOUNT_CREATED: str = "account_created"
    EMAIL_VERIFIED: str = "email_verified"
    LOGIN: str = "login"
    LOGOUT: str = "logout"
    PROFILE_UPDATED: str = "profile_updated"
    USER_PLAN_UPDATED: str = "user_plan_updated"
    TENANT_CREATED: str = "tenant_created"
    TENANT_INVITE_SENT: str = "tenant_invite_sent"
    TENANT_INVITE_ACCEPTED: str = "tenant_invite_accepted"
    TENANT_INVITE_REJECTED: str = "tenant_invite_rejected"
    TENANT_DELETED: str = "tenant_deleted"
    APP_ACTIVATED: str = "app_activated"
    APP_ACCESS_GRANTED: str = "app_access_granted"
    APP_PERMISSIONS_UPDATED: str = "app_permissions_updated"
    APP_QUOTA_UPDATED: str = "app_quota_updated"
    UPLOADER_STATUS_UPDATED: str = "uploader_status_updated"
    APP_DATA_UPDATED: str = "app_data_updated"
    DATA_SYNC_EVENTS: str = "data_sync_events"
    APP_HEALTHCHECK: str = "app_healthcheck"
    API_ERROR: str = "api_error"
    DATA_PROCESSING_LOG: str = "data_processing_log"
    DATA_STREAM: str = "data_stream"

    def dict(self):
        return asdict(self)
