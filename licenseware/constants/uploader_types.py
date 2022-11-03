from dataclasses import asdict, dataclass
from typing import List


@dataclass
class ValidationResponse:
    status: str
    filename: str
    message: str

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class FileValidationResponse:
    status: str
    message: str
    validation: List[ValidationResponse]
    event_id: str

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class FilenameValidationPayload:
    filenames: List[str]

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class FilesUploadPayload:
    files: List[bytes]

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class UploaderQuotaResponse:
    status: str
    message: str
    monthly_quota: int
    monthly_quota_consumed: int
    quota_reset_date: str
    app_id: str
    user_id: str
    uploader_id: str

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class QuotaType:
    tenant_id: str
    uploader_id: str
    monthly_quota: int
    monthly_quota_consumed: int
    quota_reset_date: str

    def dict(self):
        return asdict(self)  # pragma: no cover


@dataclass
class QuotaPlan:
    UNLIMITED: str = "UNLIMITED"
    FREE: str = "FREE"


@dataclass
class UploaderStatusResponse:
    status: str

    def dict(self):
        return asdict(self)  # pragma: no cover
