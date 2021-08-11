from marshmallow import Schema, fields


class EventSchema(Schema):
    tenant_id = fields.UUID(required=True)
    files = fields.String(required=True)
    event_type = fields.String(required=True)
    device_name = fields.String(required=False, allow_none=True)
    database_name = fields.String(required=False, allow_none=True)

