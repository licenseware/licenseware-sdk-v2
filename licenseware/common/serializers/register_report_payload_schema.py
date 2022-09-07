from marshmallow import Schema, fields, validate

from licenseware.common.serializers.report_component_filter_schema import FilterSchema
from licenseware.common.serializers.report_component_schema import ComponentSchema


class ReportSchema(Schema):
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    flags = fields.List(fields.Str, required=False)
    report_id = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    url = fields.Url(required=True)
    connected_apps = fields.List(fields.Str, required=False)
    report_components = fields.List(fields.Nested(ComponentSchema), required=False)
    filters = fields.List(fields.Nested(FilterSchema), required=False)
    preview_image_url = fields.Url(required=False, allow_none=True)
    preview_image_dark_url = fields.Url(required=False, allow_none=True)
    registrable = fields.Boolean(required=False, allow_none=True)
    private_for_tenants = fields.List(fields.Str, required=False, allow_none=True)


class RegisterReportPayloadSchema(Schema):
    data = fields.List(fields.Nested(ReportSchema), required=True)
