from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4


class PublicTokenSchema(Schema):    
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    token = fields.String(required=True, validate=validate_uuid4)
    expiration_date = fields.String(required=True)
    
    
