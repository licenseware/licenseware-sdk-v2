import base64

from marshmallow import ValidationError


def _valid_base64(sb: str):

    try:
        if not sb:
            return True
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, "ascii")
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")

        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes

    except Exception:
        return False


def validate_base64(value: str):

    if not _valid_base64(value):
        raise ValidationError("Not a valid base64 string")
