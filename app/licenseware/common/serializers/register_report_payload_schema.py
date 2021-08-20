import re
from marshmallow import (
    Schema, 
    fields, 
    validate,    
)


class ComponentSchema(Schema):
    component_id = fields.Str(required=True)
    title = fields.Str(required=True) 
    url = fields.Url(required=True)
    order = fields.Int(required=True)
    # TODO to be changed with style_props 
    style_attributes = fields.Dict(required=True)
    # TODO to be changed with data_props
    attributes = fields.Dict(required=True)
    # TODO to be changed with component_type
    type = fields.Str(required=True)
    # TODO to be changed to main_icon (data_props can contain icons too)
    icon = fields.Str(required=True)
    
    


class ReportSchema(Schema):
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    flags = fields.List(fields.Str, required=False)#, validate=validate.OneOf(flags.BETA, flags.SOON))
    report_id = fields.Str(required=True, validate=validate.Length(min=3))  
    report_name = fields.Str(required=True, validate=validate.Length(min=3))  
    description = fields.Str(required=True, validate=validate.Length(min=10))  
    url = fields.Url(required=True)
    # TODO remove from registry service this link because it's on main app definition
    # refresh_registry_url = fields.Url(required=True) 
    connected_apps = fields.List(fields.Str, required=False)
    report_components = fields.List(fields.Nested(ComponentSchema), required=False)



class RegisterReportPayloadSchema(Schema):
    data = fields.List(fields.Nested(ReportSchema), required=True)
    
    
    
    