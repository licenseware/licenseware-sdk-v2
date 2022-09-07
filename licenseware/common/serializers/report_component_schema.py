from marshmallow import Schema, fields

from licenseware.common.serializers.report_component_filter_schema import FilterSchema


class ComponentSchema(Schema):
    app_id = fields.Str(required=True)
    component_id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    url = fields.Url(required=True)
    order = fields.Int(required=True, allow_none=True)
    style_attributes = fields.Dict(required=True)
    attributes = fields.Dict(required=True)
    type = fields.Str(required=True)
    filters = fields.List(fields.Nested(FilterSchema), required=False, allow_none=True)
