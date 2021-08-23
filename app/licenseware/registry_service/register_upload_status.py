import requests
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
from app.licenseware.utils.logger import log
from app.licenseware.common.validators.registry_payload_validators import validate_register_uploader_status_payload




@authenticated_machine
def register_upload_status(tenant_id:str, status:str, uploader_id:str):

    headers = {"Authorization": envs.get_auth_token()}
    payload = {
        'data': [
            {
                'app_id': envs.APP_ID,
                'tenant_id': tenant_id,
                'upload_id': uploader_id, 
                'status': status,
            }
        ]
    }
    
    log.info(payload)
    validate_register_uploader_status_payload(payload)
    
    response = requests.post(
        url=envs.REGISTER_UPLOADER_STATUS_URL,
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        log.info("Notification registry service success!")
        return {"status": "success", "message": payload, "content": payload}, 200
    
    log.error("Notification registry service failed!")
    return {"status": "fail", "message": payload, "content": payload}, 500
