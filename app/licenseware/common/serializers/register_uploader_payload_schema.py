from marshmallow import (
    Schema, 
    fields, 
    validate,  #utils validatiors
)

from app.licenseware.common.constants import states, flags
from app.licenseware.common.validators import validate_route, validate_icon



class UploaderInfoSchema(Schema):
    
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    upload_id = fields.Str(required=True, validate=validate.Length(min=3))
    # TODO change it to uploader_id for registry service
    # uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    upload_name = fields.Str(required=True, validate=validate.Length(min=3))  
    # TODO change it to name in registry service
    # name = fields.Str(required=True, validate=validate.Length(min=3))  
    description = fields.Str(required=True, validate=validate.Length(min=10))
    flags = fields.List(fields.Str, required=False, validate=validate.OneOf(flags.BETA, flags.SOON))
    accepted_file_types = fields.List(fields.Str, required=True)
    upload_url = fields.Str(required=True, validate=validate_route)
    upload_validation_url = fields.Str(required=True, validate=validate_route)
    quota_validation_url = fields.Str(required=True, validate=validate_route)
    status_check_url = fields.Str(required=True, validate=validate_route)
    icon = fields.Str(required=False, validate=validate_icon)
    status = fields.Str(required=False, validate=validate.OneOf(states.IDLE, states.RUNNING))


class RegisterUploaderPayloadSchema(Schema):
    data = fields.List(fields.Nested(UploaderInfoSchema), required=True)
    



