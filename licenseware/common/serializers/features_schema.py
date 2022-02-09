from marshmallow import Schema, fields
from licenseware.common.validators import validate_uuid4


class FeaturesSchema(Schema):
    tenant_id = fields.String(required=True, validate=validate_uuid4)
    