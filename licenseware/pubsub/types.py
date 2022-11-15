from dataclasses import asdict, dataclass

# Only CamelCase here - kafka throws a warning for '-' and '_'


@dataclass
class TopicType:
    # This needs to be in sync with stack-manager-v2/scripts/kafka/kafka-topics.csv
    # These topics are created on kafka startup
    USER_EVENTS: str = "UserEvents"
    APP_EVENTS: str = "AppEvents"
    LOG_EVENTS: str = "LogEvents"
    DATA_STREAM: str = "DataStream"

    def dict(self):
        return asdict(self)  # pragma no cover


@dataclass
class EventType:

    ACCOUNT_CREATED: str = "AccountCreated"
    EMAIL_VERIFIED: str = "EmailVerified"
    LOGIN: str = "Login"
    LOGOUT: str = "Logout"
    PROFILE_UPDATED: str = "ProfileUpdated"
    USER_PLAN_UPDATED: str = "UserPlanUpdated"
    TENANT_CREATED: str = "TenantCreated"
    TENANT_INVITE_SENT: str = "TenantInviteSent"
    TENANT_INVITE_ACCEPTED: str = "TenantInviteAccepted"
    TENANT_INVITE_REJECTED: str = "TenantInviteRejected"
    TENANT_DELETED: str = "TenantDeleted"
    APP_ACTIVATED: str = "AppActivated"
    APP_ACCESS_GRANTED: str = "AppAccessGranted"
    APP_PERMISSIONS_UPDATED: str = "AppPermissionsUpdated"
    APP_QUOTA_UPDATED: str = "AppQuotaUpdated"

    APP_FULL_METADATA: str = "AppFullMetadata"
    APP_METADATA: str = "AppMetadata"
    ULOADER_METADATA: str = "UploaderMetadata"
    REPORT_METADATA: str = "ReportMetadata"
    REPORT_COMPONENT_METADATA: str = "ReportMetadata"

    NEW_NOTIFICATION: str = "NewNotification"
    UPLOADER_STATUS_UPDATED: str = "UploaderStatusUpdated"
    REPORT_DATA_AVAILABLE: str = "ReportDataAvailable"
    APP_DATA_UPDATED: str = "AppDataUpdated"
    DATA_SYNC_EVENTS: str = "DataSyncEvents"
    APP_HEALTHCHECK: str = "AppHealthCheck"
    API_ERROR: str = "ApiError"
    DATA_PROCESSING_LOG: str = "DataProcessingLog"
    DATA_STREAM: str = "DataStream"

    def dict(self):
        return asdict(self)  # pragma no cover
