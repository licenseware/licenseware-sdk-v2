from .base_enum import BaseEnum


class States(BaseEnum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"
    ENABLED = "enabled"
    DISABLED = "disabled"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ACTION_REQUIRED = "action_required"
    REQUEST_ACCEPTED = "accepted"
    REQUEST_REJECTED = "rejected"
    REQUEST_PENDING = "pending"
    REQUEST_REQUESTED = "requested"
    REQUEST_CANCELLED = "cancelled"
    REQUEST_REVOKED = "revoked"
