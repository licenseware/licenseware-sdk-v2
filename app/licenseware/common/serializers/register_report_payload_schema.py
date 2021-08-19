from marshmallow import (
    Schema, 
    fields, 
    validate,    
)


class ReportSchema(Schema):
    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    flags = fields.List(fields.Str, required=False)#, validate=validate.OneOf(flags.BETA, flags.SOON))
    # id = fields.Str(required=True, validate=validate.Length(min=3))  
    # name = fields.Str(required=True, validate=validate.Length(min=3))  
    # TODO change in registry service field names without report_prefix
    report_id = fields.Str(required=True, validate=validate.Length(min=3))  
    report_name = fields.Str(required=True, validate=validate.Length(min=3))  
    description = fields.Str(required=True, validate=validate.Length(min=10))  
    url = fields.Url(required=True)
    refresh_registry_url = fields.Url(required=True) # does this refresh the reports data?
    connected_apps = fields.List(fields.Str, required=False)


class RegisterReportPayloadSchema(Schema):
    data = fields.List(fields.Nested(ReportSchema), required=True)
    
    
    
    