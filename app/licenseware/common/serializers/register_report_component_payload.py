from marshmallow import Schema, fields




class ComponentSchema(Schema):
    app_id = fields.Str(required=True)
    component_id = fields.Str(required=True)
    title = fields.Str(required=True) 
    url = fields.Url(required=True)
    order = fields.Int(required=True, allow_none=True)
    style_attributes = fields.Dict(required=True)
    attributes = fields.Dict(required=True)
    type = fields.Str(required=True)
    
    
class RegisterReportComponentPayloadSchema(Schema):
    data = fields.List(fields.Nested(ComponentSchema), required=True)
