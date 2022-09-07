from marshmallow import Schema, fields

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class FileNameValidationSchema(Schema):
    status = fields.String()
    filename = fields.String()
    message = fields.String()


class FileContentValidationSchema(Schema):
    status = fields.String()
    filename = fields.String()
    filepath = fields.String()
    message = fields.String()


class ProcessingDetailsSchema(Schema):
    step = fields.String(required=True)
    filepath = fields.String(required=True)
    status = fields.String(required=True)
    # Permisive on_success_save and on_failure_save
    success = fields.Raw(required=False, allow_none=True)
    error = fields.Raw(required=False, allow_none=True)
    traceback = fields.String(required=False, allow_none=True)
    callable = fields.String(required=False, allow_none=True)
    source = fields.String(required=False, allow_none=True)
    updated_at = fields.String(required=True)
    file_name = fields.String(required=True)


class HistorySchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    event_id = fields.String(required=True, validate=validate_uuid4)
    app_id = fields.String(required=True)
    uploader_id = fields.String(required=True)
    filename_validation = fields.List(fields.Nested(FileNameValidationSchema))
    file_content_validation = fields.List(fields.Nested(FileContentValidationSchema))
    files_uploaded = fields.List(fields.String)
    processing_details = fields.List(
        fields.Nested(ProcessingDetailsSchema), allow_none=True
    )
    updated_at = fields.String()
    filename_validation_updated_at = fields.String()
    file_content_validation_updated_at = fields.String()


class EntitiesSchema(Schema):
    entities = fields.List(fields.Raw, required=True)
