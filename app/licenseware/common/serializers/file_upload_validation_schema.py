from marshmallow import (
    Schema, 
    fields, 
    validate
)

from app.licenseware.common.constants import states


class FileValidationSchema(Schema):
    filename = fields.Str(required=True, validate=validate.Length(min=5))
    status   = fields.Str(required=True, validate=validate.OneOf(states.SUCCESS, states.FAIL)) 
    message  = fields.Str(required=True, validate=validate.Length(min=10))
    

class FileUploadValidationSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(states.SUCCESS, states.FAIL)) 
    message = fields.Str(required=True, validate=validate.Length(min=10))
    validation = fields.List(fields.Nested(FileValidationSchema), required=True)
    units = fields.Int(requred=True)
    
