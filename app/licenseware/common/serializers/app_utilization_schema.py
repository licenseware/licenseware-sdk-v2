from marshmallow import Schema, fields


class AppUtilizationSchema(Schema):
    _id = fields.Str(required=True)
    tenant_id = fields.UUID(required=True)
    unit_type = fields.Str(required=True)
    monthly_quota = fields.Int(required=True) 
    monthly_quota_consumed = fields.Int(required=True) 
    quota_reset_date = fields.Str(required=True)

