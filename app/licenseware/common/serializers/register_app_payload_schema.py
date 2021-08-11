from marshmallow import (
    Schema, 
    fields, 
    validate,       #utils validatiors
    validates,      #decorator  
    ValidationError #custom exception
)

def validate_route(value):
    if not value.startswith('/') and len(value) < 2:
        raise ValidationError("Routes must start with '/'")
    

class AppActivatedTenantsSchema(Schema): ... #TODO
class DataAvailableTenantsSchema(Schema): ...#TODO


class AppInfoSchema(Schema):
    
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(required=True, validate=validate.Length(min=3))  
    tenants_with_app_activated = fields.List(fields.Dict, required=True) #TODO
    tenants_with_data_available = fields.List(fields.Dict, required=True) #TODO
    description = fields.Str(required=True, validate=validate.Length(min=10))
    flags = fields.List(fields.Str, required=False) #TODO add oneOf validator
    icon = fields.Str(required=False, validate=validate.Length(min=5))
    refresh_registration_url = fields.Str(required=True, validate=validate_route)
    app_activation_url = fields.Str(required=True, validate=validate_route)
    editable_tables_url = fields.Str(required=True, validate=validate_route)
    history_report_url = fields.Str(required=True, validate=validate_route)
    tenant_registration_url = fields.Str(required=True, validate=validate_route)

    @validates("icon")
    def validate_quantity(self, value):
        accepted_icon_types = ('.png', '.svg', '.jpg', '.jpeg', '.webp')
        if not value.endswith(accepted_icon_types):
            raise ValidationError(f"Icons must be of type {accepted_icon_types}")
    


class RegisterAppPayloadSchema(Schema):
    data = fields.List(fields.Nested(AppInfoSchema), required=True)
    


