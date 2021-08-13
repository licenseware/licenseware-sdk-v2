from app.licenseware.utils.logger import log
from marshmallow import Schema


def schema_validator(schema:Schema, data:dict, raise_error=True):
    
    # ok_msg = "Validation of register app payload successful"
    nok_msg = lambda err: f"Validation failed \n {err}"
    
    if raise_error:
        schema().load(data)
        # log.success(ok_msg)
        return True
    else:
        try:
            schema().load(data)
            # log.success(ok_msg)
            return True
        except Exception as err:
            log.error(nok_msg(err))
            return False

    
    