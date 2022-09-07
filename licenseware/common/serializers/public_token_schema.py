from marshmallow import Schema, fields

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class PublicTokenSchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    app_id = fields.String(required=True)
    report_id = fields.String(required=True)
    token = fields.String(required=True)
    expiration_date = fields.String(required=True)
