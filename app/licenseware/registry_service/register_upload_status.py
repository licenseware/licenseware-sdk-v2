import requests
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
from app.licenseware.utils.logger import log
from app.licenseware.common.validators.registry_payload_validators import validate_register_uploader_status_payload




@authenticated_machine
def register_upload_status(**kwargs):
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
        
        
    payload = {
        'data': [
            {
                'app_id': envs.APP_ID,
                'tenant_id': kwargs['tenant_id'],
                'upload_id': kwargs['uploader_id'], 
                'status': kwargs['status'],
            }
        ]
    }
    
    log.info(payload)
    validate_register_uploader_status_payload(payload)
    
    headers = {"Authorization": envs.get_auth_token()}
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

