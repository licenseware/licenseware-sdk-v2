from marshmallow import ValidationError
from uuid import UUID
import random


def _valid_uuid(value):
    try:
        if not value: return True
        if isinstance(value, str):
            UUID(value)
        elif isinstance(value, list) and value:
            UUID(random.choice(value)) # optimistic validation
        else:
            raise ValidationError("Not a valid uuid4 string")
        return True
    except ValueError:
        return False


def validate_uuid4(value):
    if not _valid_uuid(value):
        raise ValidationError("Not a valid uuid4 string")
    
