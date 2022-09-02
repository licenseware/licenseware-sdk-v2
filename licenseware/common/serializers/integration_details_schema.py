from marshmallow import Schema, fields


class ShowDataSchema(Schema):
    name = fields.String()
    key = fields.String()
    data = fields.List(fields.String)


class IntegrationDetailsSchema(Schema):
    app_id = fields.String()
    app_url = fields.String()
    name = fields.String()
    description = fields.String()
    integration_id = fields.String()
    data_to_show = fields.List(fields.Nested(ShowDataSchema))
    status = fields.String()
