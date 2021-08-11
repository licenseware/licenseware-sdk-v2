from app.licenseware.utils.logger import log
from app.licenseware.common.serializers import RegisterAppPayloadSchema



def validate_register_app_payload(payload:dict, raise_error=True):
    
    # ok_msg = "Validation of register app payload successful"
    nok_msg = lambda err: f"Validation of register app payload failed \n {err}"
    
    if raise_error:
        RegisterAppPayloadSchema().load(payload)
        # log.success(ok_msg)
        return True
    else:
        try:
            RegisterAppPayloadSchema().load(payload)
            # log.success(ok_msg)
            return True
        except Exception as err:
            log.error(nok_msg(err))
            return False

    
    