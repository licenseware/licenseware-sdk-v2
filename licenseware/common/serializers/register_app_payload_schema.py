from marshmallow import (
    Schema, 
    fields, 
    validate,       #utils validators
    validates,      #decorator  
)

from licenseware.common.constants import flags
from licenseware.common.validators import validate_icon, validate_uuid4



    
class DataAvailableTenantsSchema(Schema): 
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    last_update_date = fields.Str(required=True)
    


class AppInfoSchema(Schema):
    
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(required=True, validate=validate.Length(min=3))  
    tenants_with_app_activated = fields.List(fields.Str, validate=validate_uuid4, required=True) 
    tenants_with_data_available = fields.List(fields.Nested(DataAvailableTenantsSchema), required=True) 
    description = fields.Str(required=True, validate=validate.Length(min=10))
    flags = fields.List(fields.Str, required=False)#, validate=validate.OneOf(flags.BETA, flags.SOON))
    icon = fields.Str(required=False, validate=validate_icon)
    refresh_registration_url = fields.Url(required=True)
    app_activation_url = fields.Url(required=True)
    editable_tables_url = fields.Url(required=True)
    history_report_url = fields.Url(required=True)
    tenant_registration_url = fields.Url(required=True)
    terms_and_conditions_url = fields.Url(required=True)
    

    

class RegisterAppPayloadSchema(Schema):
    data = fields.List(fields.Nested(AppInfoSchema), required=True)
    


