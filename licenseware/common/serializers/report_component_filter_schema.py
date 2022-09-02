from marshmallow import Schema, fields


class FilterSchema(Schema):
    column = fields.Str(required=True)
    allowed_filters = fields.List(fields.Str, required=True)
    visible_name = fields.Str(required=True)
    # TODO column_type must be set on filters, allow_none it's a temporary fix
    column_type = fields.Str(required=True, allow_none=True)
    allowed_values = fields.List(fields.Str, required=False, allow_none=True)
