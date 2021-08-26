from marshmallow import Schema, fields

#TODO

class AnalysisStatusSchema(Schema):
    tenant_id = fields.UUID(required=True)
    status = fields.Str(required=True)
    uploader_id = fields.Str(required=False)
    
    
