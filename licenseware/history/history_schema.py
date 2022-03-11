from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4


class FileNameValidationSchema(Schema):
    pass


class FileContentValidationSchema(Schema):
    pass


class ProcessingDetailsSchema(Schema):
    step = fields.String()
    error = fields.String()
    processed_file_path = fields.String()
    traceback = fields.String()


class HistorySchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    event_id = fields.String(required=True, validate=validate_uuid4)
    uploader_id = fields.String(required=True)
    filename_validation = fields.List(fields.Nested(FileNameValidationSchema))
    file_content_validation = fields.List(fields.Nested(FileContentValidationSchema))
    files_uploaded = fields.List(fields.String)
    processing_details = fields.List(fields.Nested(ProcessingDetailsSchema))


"""
{
    "tenant_id": "xxx",
    "event_id": "xxxx",
    "uploader_id": "rv_lite",
    "entities_ids": [
        "uuid4 strings"
    ],
    "filename_validation": [
        {"file_path": "/path/file", "response": the filename validation response},
        etc
    ],
    "file_content_validationr bulk file should look:": [
        {"file_path": "/path/file", "response": the file content validation response},
        etc
    ],
    "files_uploaded": [file_path1, file_path2, file_path3],
    "processing_details": [
            {
                "step": "Getting machines CPU cores",
                "error": "Value in column x not an integer",
                "processed_file_path": "path/to/file/processed",
                "traceback": "traceback error"
            }
            etc
    ]
}
"""