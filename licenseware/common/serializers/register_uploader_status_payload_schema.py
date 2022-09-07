from marshmallow import Schema, fields, validate

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class UploaderStatusSchema(Schema):

    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    status = fields.Str(required=True)


class RegisterUploaderStatusPayloadSchema(Schema):
    data = fields.List(fields.Nested(UploaderStatusSchema), required=True)
