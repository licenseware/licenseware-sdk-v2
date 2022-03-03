from marshmallow import Schema, fields
from .report_component_schema import ComponentSchema


class RegisterReportComponentPayloadSchema(Schema):
    data = fields.List(fields.Nested(ComponentSchema), required=True)
