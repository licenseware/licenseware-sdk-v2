from marshmallow import Schema, fields
from app.licenseware.common.validators import validate_uuid4


#TODO


class AnalysisStatusSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    status = fields.Str(required=True)
    uploader_id = fields.Str(required=False)
    
    
