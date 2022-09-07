from bson.objectid import ObjectId
from marshmallow import ValidationError

from licenseware.common.validators.validate_uuid4 import validate_uuid4


def valid__id(value):
    try:
        validate_uuid4(value)
        return True
    except (ValidationError, ValueError):
        try:
            ObjectId(value)
            return True
        except (ValidationError, ValueError):
            return False


def validate__id(value):
    if not valid__id(value):
        raise ValidationError("Not a valid uuid4 or objectId string")
