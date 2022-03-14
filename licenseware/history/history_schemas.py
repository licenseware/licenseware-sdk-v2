from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4


class FileNameValidationSchema(Schema):
    status = fields.String
    filename = fields.String
    message = fields.String


class FileContentValidationSchema(Schema):
    status = fields.String
    filename = fields.String
    filepath = fields.String
    message = fields.String


class ProcessingDetailsSchema(Schema):
    step = fields.String
    filepath = fields.String
    status = fields.String
    success = fields.String
    error = fields.String
    traceback = fields.String
    callable = fields.String
    source = fields.String


class HistorySchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    event_id = fields.String(required=True, validate=validate_uuid4)
    app_id = fields.String(required=True)
    uploader_id = fields.String(required=True)
    filename_validation = fields.List(fields.Nested(FileNameValidationSchema))
    file_content_validation = fields.List(fields.Nested(FileContentValidationSchema))
    files_uploaded = fields.List(fields.String)
    processing_details = fields.List(fields.Nested(ProcessingDetailsSchema))


"""
Example:

{
    "tenant_id": metadata["tenant_id"],
    "event_id": metadata["event_id"],
    "app_id": metadata["app_id"],
    "uploader_id": metadata["uploader_id"],
    "filename_validation": [
            {
              "status": "success",
              "filename": "rvtools.xlsx",
              "message": "Filename is valid"
            },
            {
              "status": "success",
              "filename": "options.csv",
              "message": "Filename is valid"
            }
    ],
    "file_content_validation": [
        {
          "status": "success",
          "filename": "cpuq.txt",
          "filepath": "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt",
          "message": "Filename is valid"
        }
    ],
    "files_uploaded": response["event_data"]["filepaths"],
    "processing_details": [{
        "step": metadata['step'],
        "filepath": metadata["filepath"],
        "status": response["status"],
        "success": response["success"],
        "error": response["error"],
        "traceback": response["traceback"],
        "callable": metadata['callable'],
        "source": metadata['source']
    }]
}

"""
