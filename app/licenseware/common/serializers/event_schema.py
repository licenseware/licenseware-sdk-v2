from marshmallow import Schema, fields, validate
from app.licenseware.common.validators import validate_uuid4


class EventSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    files = fields.Str(required=True, validate=validate.Length(min=5))
    uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    device_name = fields.Str(required=False, allow_none=True)
    database_name = fields.Str(required=False, allow_none=True)

