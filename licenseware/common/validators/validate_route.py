from marshmallow import ValidationError


def validate_route(value):
    if not value.startswith("/") and len(value) < 2:
        raise ValidationError("Routes must start with '/'")
