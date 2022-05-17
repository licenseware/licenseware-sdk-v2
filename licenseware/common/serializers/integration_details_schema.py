from marshmallow import Schema, fields


class IntegrationDetailsSchema(Schema):
    app_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    integration_id = fields.String(required=True)
    imported_data = fields.List(fields.String, required=True)
    exported_data = fields.List(fields.String, required=True)
    triggers = fields.List(fields.String, required=True)
    