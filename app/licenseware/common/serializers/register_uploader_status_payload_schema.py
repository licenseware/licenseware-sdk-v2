from marshmallow import (
    Schema, 
    fields, 
    validate
)

from app.licenseware.common.constants import states
from app.licenseware.common.validators import validate_uuid4



class UploaderStatusSchema(Schema):
    
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    #TODO change in registry service from upload_id to uploader_id
    upload_id = fields.Str(required=True, validate=validate.Length(min=3))
    status = fields.Str(required=False, validate=validate.OneOf(states.IDLE, states.RUNNING))



class RegisterUploaderStatusPayloadSchema(Schema):
    data = fields.List(fields.Nested(UploaderStatusSchema), required=True)
    
