from marshmallow import Schema, fields

from licenseware.common.serializers.report_component_schema import ComponentSchema


class RegisterReportComponentPayloadSchema(Schema):
    data = fields.List(fields.Nested(ComponentSchema), required=True)
