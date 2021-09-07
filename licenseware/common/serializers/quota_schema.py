from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4




class QuotaSchema(Schema):
    user_id = fields.Str(required=True, validate=validate_uuid4)
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    uploader_id = fields.Str(required=True)
    monthly_quota = fields.Int(required=True) 
    monthly_quota_consumed = fields.Int(required=True) 
    quota_reset_date = fields.Str(required=True)
