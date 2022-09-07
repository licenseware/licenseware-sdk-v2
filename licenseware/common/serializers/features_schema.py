from marshmallow import Schema, fields

from licenseware.common.validators.validate_uuid4 import validate_uuid4


class FeaturesSchema(Schema):

    tenant_id = fields.String(required=True, validate=validate_uuid4)
    name = fields.String(required=True)
    app_id = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    access_levels = fields.List(fields.String, required=False, allow_none=True)
    monthly_quota = fields.Integer(required=False, allow_none=True)
    activated = fields.Boolean(required=False, allow_none=True)
    feature_id = fields.String(required=False, allow_none=True)
    feature_path = fields.String(required=False, allow_none=True)
