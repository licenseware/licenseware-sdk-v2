import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.common.validators.registry_payload_validators import validate_register_uploader_payload




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
        
        
    app_id = envs.APP_ID + envs.PERSONAL_SUFFIX if envs.environment_is_local() else envs.APP_ID
    uploader_id = kwargs['uploader_id'] + envs.PERSONAL_SUFFIX if envs.environment_is_local() else kwargs['uploader_id']
    
    payload = {
        'data': [{
            "app_id": app_id,
            "upload_name": kwargs['name'],
            "description": kwargs['description'],
            "accepted_file_types": kwargs['accepted_file_types'],
            "upload_id": uploader_id,
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
            "message": f"Uploader '{kwargs['uploader_id']}' register successfully",
            "content": payload
        }, 200


    nokmsg = f"Could not register uploader '{kwargs['uploader_id']}'"
    log.error(nokmsg)
    return {"status": "fail", "message": nokmsg, "content": payload}, 400






