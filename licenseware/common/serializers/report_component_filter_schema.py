from marshmallow import Schema, fields



class FilterSchema(Schema):
    column = fields.Str(required=True)
    allowed_filters = fields.List(fields.Str, required=True)
    visible_name = fields.Str(required=True)
    column_type = fields.Str(required=True)
    