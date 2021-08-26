from marshmallow import ValidationError
from uuid import UUID


def _valid_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


def validate_uuid4(value):
    if not _valid_uuid(value):
        raise ValidationError(f"{value} is not a valid uuid4 string")
    
