from enum import Enum
from typing import List, Union

from pydantic import BaseModel


class EventTypes(str, Enum):
    FILE_VALIDATION = "FileValidation"
    PROCESSING_DETAILS = "ProcessingDetails"
    ENTITIES_EXTRACTED = "EntitiesExtracted"


class Status(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class HistoryFilesSchema(BaseModel):
    filepath: str
    filename: str


class HistorySchema(BaseModel):
    app_id: str
    uploader_id: str
    app_name: str
    uploader_name: str
    tenant_id: str
    event_id: str
    event_type: EventTypes
    description: str  # "docstring" or "funcname" parsed extracting_devices > Extracting Devices
    updated_at: str
    step: str = None  # "1 of 12"
    status: Status = Status.SUCCESS
    files: List[HistoryFilesSchema] = None
    entities: List[Union[str, dict]] = None
    processing_time: str = None
    source: str = None
    func_args: list = None
    func_kwargs: dict = None
    error: str = None
    traceback: str = None


"""
[
    {
        "app_id": "fmw-service",
        "uploader_id": "lms_collection_archive",
        "app_name": "Oracle Middleware Manager",
        "uploader_name": "Oracle LMS Collection",
        "tenant_id": "fd101438-d7f5-4a8e-8280-a1769a9a7833",
        "event_id": "cd915689-0499-47f3-8baa-e073332c0c4c",

        "log_type": "file_content_validation",
        "status": "success",
        "files": [
            {
                "filepath": "/tmp/otgpptp/options.csv",
                "filename": "options.csv"
            },
            {
                "filepath": "/tmp/otgpptp/options.csv",
                "filename": "version.csv"
            },
        ]
    },
    {
        "app_id": "fmw-service",
        "uploader_id": "lms_collection_archive",
        "app_name": "Oracle Middleware Manager",
        "uploader_name": "Oracle LMS Collection",
        "tenant_id": "fd101438-d7f5-4a8e-8280-a1769a9a7833",
        "event_id": "cd915689-0499-47f3-8baa-e073332c0c4c",

        "log_type": "file_content_validation",
        "status": "fail",
        "files": [
            {
                "filepath": "/tmp/otgpptp/options.csv",
                "filename": "dba_feature.csv"
            }
        ]
    },
    {
        "app_id": "fmw-service",
        "uploader_id": "lms_collection_archive",
        "app_name": "Oracle Middleware Manager",
        "uploader_name": "Oracle LMS Collection",
        "tenant_id": "fd101438-d7f5-4a8e-8280-a1769a9a7833",
        "event_id": "cd915689-0499-47f3-8baa-e073332c0c4c",

        "log_type": "processing_details",
        "step": "1 of 12",
        "description": "docstring",
        "status": "success",
        "files": [
            {
                "filepath": "/tmp/otgpptp/options.csv",
                "filename": "dba_feature.csv"
            }
        ]
    },
    {
        "app_id": "fmw-service",
        "uploader_id": "lms_collection_archive",
        "app_name": "Oracle Middleware Manager",
        "uploader_name": "Oracle LMS Collection",
        "tenant_id": "fd101438-d7f5-4a8e-8280-a1769a9a7833",
        "event_id": "cd915689-0499-47f3-8baa-e073332c0c4c",

        "log_type": "entities_extracted",
        "entity_type": "device",
        "entities": ["dev1", "dev20"]
        "files": [
            {
                "filepath": "/tmp/otgpptp/options.csv",
                "filename": "dba_feature.csv"
            }
        ]
    },
]

"""
