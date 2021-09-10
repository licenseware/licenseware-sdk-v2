from marshmallow import Schema, fields, validate
from licenseware.common.validators import validate_uuid4


class EventSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    filepaths = fields.List(fields.Str, required=True)
    uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    flask_request = fields.Dict(required=False, allow_none=True)
    validation_response = fields.Dict(required=False, allow_none=True)
    