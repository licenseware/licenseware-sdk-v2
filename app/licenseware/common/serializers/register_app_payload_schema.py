from marshmallow import (
    Schema, 
    fields, 
    validate,       #utils validatiors
    validates,      #decorator  
)

from app.licenseware.common.validators import validate_route, validate_icon


class AppActivatedTenantsSchema(Schema): ... #TODO
class DataAvailableTenantsSchema(Schema): ...#TODO


class AppInfoSchema(Schema):
    
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(required=True, validate=validate.Length(min=3))  
    tenants_with_app_activated = fields.List(fields.Dict, required=True) #TODO
    tenants_with_data_available = fields.List(fields.Dict, required=True) #TODO
    description = fields.Str(required=True, validate=validate.Length(min=10))
    flags = fields.List(fields.Str, required=False) #TODO add oneOf validator
    icon = fields.Str(required=False, validate=validate_icon)
    refresh_registration_url = fields.Str(required=True, validate=validate_route)
    app_activation_url = fields.Str(required=True, validate=validate_route)
    editable_tables_url = fields.Str(required=True, validate=validate_route)
    history_report_url = fields.Str(required=True, validate=validate_route)
    tenant_registration_url = fields.Str(required=True, validate=validate_route)

    

class RegisterAppPayloadSchema(Schema):
    data = fields.List(fields.Nested(AppInfoSchema), required=True)
    


