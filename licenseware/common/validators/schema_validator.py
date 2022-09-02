import traceback
from typing import Any

from licenseware.utils.logger import log


def validate_data(schema: type, data: Any):
    if isinstance(data, dict):
        data = schema().load(data)
        return data

    if isinstance(data, list):
        data = schema(many=True).load(data)
        return data

    raise Exception("Data sent for validation must be wither a dict or a list")


def schema_validator(schema: type, data: dict, raise_error=True):
    """
    Using Marshmallow schema class to validate data (dict or list of dicts)
    """

    nok_msg = lambda err: f"Validation failed \n {err}"

    if raise_error:
        validate_data(schema, data)
        return True
    else:
        try:
            validate_data(schema, data)
            # log.success(ok_msg)
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False
