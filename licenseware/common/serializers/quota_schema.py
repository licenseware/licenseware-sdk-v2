from marshmallow import Schema, fields

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class QuotaSchema(Schema):
    _id = fields.Str(required=False)
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    uploader_id = fields.Str(required=True)
    monthly_quota = fields.Int(required=True)
    monthly_quota_consumed = fields.Int(required=True)
    quota_reset_date = fields.Str(required=True)
