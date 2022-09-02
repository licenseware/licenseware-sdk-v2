from marshmallow import ValidationError


def validate_icon(value):
    accepted_icon_types = (".png", ".svg", ".jpg", ".jpeg", ".webp")
    if not value.endswith(accepted_icon_types):
        raise ValidationError(f"Icons must be of type {accepted_icon_types}")
