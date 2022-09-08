from marshmallow import Schema, fields

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class AnalysisStatusSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    status = fields.Str(required=True)
    uploader_id = fields.Str(required=False)
