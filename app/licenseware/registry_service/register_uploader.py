import requests
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
from app.licenseware.common.validators.registry_payload_validators import validate_register_uploader_payload




@authenticated_machine
def register_uploader(**kwargs):
    """
        Send a post request to registry service to make uploader available in front-end
    """
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
        
        
    payload = {
        'data': [{
            "app_id": envs.APP_ID,
            "upload_name": kwargs['name'],
            "description": kwargs['description'],
            "accepted_file_types": kwargs['accepted_file_types'],
            "upload_id": kwargs['uploader_id'],
            "flags": kwargs['flags'],
            "status": kwargs['status'],
            "icon": kwargs['icon'],
            "upload_url": kwargs['upload_url'],
            "upload_validation_url": kwargs['upload_validation_url'],
            "quota_validation_url": kwargs['quota_validation_url'],
            "status_check_url": kwargs['status_check_url']
        }]
    }

    log.info(payload)
    validate_register_uploader_payload(payload)
    
    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_UPLOADER_URL, json=payload, headers=headers)


    if registration.status_code == 200:
        return {
            "status": "success",
            "message": f"Uploader '{kwargs['uploader_id']}' register successfully"
        }, 200


    nokmsg = f"Could not register uploader '{kwargs['uploader_id']}'"
    log.error(nokmsg)
    return {"status": "fail", "message": nokmsg}, 400






