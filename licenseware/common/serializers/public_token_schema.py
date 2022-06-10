from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4


class PublicTokenSchema(Schema):    
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    report_id = fields.String(required=True)
    token = fields.String(required=True)
    expiration_date = fields.String(required=True)
    
    
