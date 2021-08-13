from marshmallow import Schema, fields, validate


class EventSchema(Schema):
    tenant_id = fields.UUID(required=True)
    files = fields.Str(required=True, validate=validate.Length(min=5))
    uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    device_name = fields.Str(required=False, allow_none=True)
    database_name = fields.Str(required=False, allow_none=True)

