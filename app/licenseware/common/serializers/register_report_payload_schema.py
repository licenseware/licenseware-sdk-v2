from app.licenseware.common.serializers.report_component_filter_schema import FilterSchema
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
    style_attributes = fields.Dict(required=True)
    attributes = fields.Dict(required=True)
    type = fields.Str(required=True)
    icon = fields.Str(required=False) #is icon only on series?
    filters = fields.List(fields.Nested(FilterSchema), required=False)
    


class ReportSchema(Schema):
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    flags = fields.List(fields.Str, required=False)#, validate=validate.OneOf(flags.BETA, flags.SOON))
    report_id = fields.Str(required=True, validate=validate.Length(min=3))  
    report_name = fields.Str(required=True, validate=validate.Length(min=3))  
    description = fields.Str(required=True, validate=validate.Length(min=10))  
    url = fields.Url(required=True)
    connected_apps = fields.List(fields.Str, required=False)
    report_components = fields.List(fields.Nested(ComponentSchema), required=False)
    filters = fields.List(fields.Nested(FilterSchema), required=False)
    

class RegisterReportPayloadSchema(Schema):
    data = fields.List(fields.Nested(ReportSchema), required=True)
    
    
    
    