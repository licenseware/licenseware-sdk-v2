from marshmallow import (
    Schema, 
    fields, 
    validate,  #utils validatiors
)

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
    flags = fields.List(fields.Str, required=False) #TODO add oneOf validator
    accepted_file_types = fields.List(fields.Str, required=True)
    upload_url = fields.Str(required=True, validate=validate_route)
    upload_validation_url = fields.Str(required=True, validate=validate_route)
    quota_validation_url = fields.Str(required=True, validate=validate_route)
    status_check_url = fields.Str(required=True, validate=validate_route)
    icon = fields.Str(required=False, validate=validate_icon)
    status = fields.Str(required=False) #TODO add oneOf validator


class RegisterUploaderPayloadSchema(Schema):
    data = fields.List(fields.Nested(UploaderInfoSchema), required=True)
    




"""
payload = {
    'data': [{
        # "app_id": self.app_id,
        # name < "upload_name": self.upload_name,
        # uploader_id < "upload_id": self.uploader_id, #TODO Field to be later renamed to uploader_id
        # "accepted_file_types": self.accepted_file_types,
        # "description": self.description,
        # "flags": self.flags,
        # "upload_url": self.base_url + self.upload_url,
        # "upload_validation_url": self.base_url + self.upload_validation_url,
        # "quota_validation_url": self.base_url + self.quota_validation_url,
        # "status_check_url": self.base_url + self.status_check_url,
        # "history_url": self.base_url + self.history_url, TODO not neeeded anymore
        "status": self.status,
        # "icon": self.icon,
    }]
}

"""
