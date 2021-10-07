import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.common.validators.registry_payload_validators import validate_register_uploader_payload


def _get_validation_parameters(validator_class):
    
    if not hasattr(validator_class, 'vars'): return {}
    
    validators = vars(validator_class)
    
    params_list = [
        'filename_contains',
        'filename_endswith',
        'ignore_filenames',
        'required_input_type',
        'required_sheets',
        'required_columns',
        'text_contains_all',
        'text_contains_any',
        'min_rows_number',
        'header_starts_at',
        'buffer',
        'filename_valid_message',
        'filename_invalid_message',
        'filename_ignored_message'                                        
    ]
    
    return {k:v for k,v in validators.items() if k in params_list}

    


@authenticated_machine
def register_uploader(single_request=True, **kwargs):
    """
        Send a post request to registry service to make uploader available in front-end
    """
    
    validation_parameters = _get_validation_parameters(kwargs['validator_class'])
    
    app_id = envs.APP_ID + envs.PERSONAL_SUFFIX if envs.environment_is_local() else envs.APP_ID
    uploader_id = kwargs['uploader_id'] + envs.PERSONAL_SUFFIX if envs.environment_is_local() else kwargs['uploader_id']
    
    payload = {
        'data': [{
            "app_id": app_id,
            "upload_name": kwargs['name'],
            "description": kwargs['description'],
            "accepted_file_types": kwargs['accepted_file_types'],
            "upload_id": uploader_id,
            "flags": kwargs['flags'] if len(kwargs['flags']) > 0 else None,
            "status": kwargs['status'],
            "icon": kwargs['icon'],
            "upload_url": kwargs['upload_url'],
            "upload_validation_url": kwargs['upload_validation_url'],
            "quota_validation_url": kwargs['quota_validation_url'],
            "status_check_url": kwargs['status_check_url'],
            "validation_parameters": validation_parameters
        }]
    }

    if single_request: log.info(payload)    
    validate_register_uploader_payload(payload)
    
    headers = {"Authorization": envs.get_auth_token()}
    post_kwargs = dict(url=envs.REGISTER_UPLOADER_URL, json=payload, headers=headers)
    
    if single_request:
        registration = requests.post(**post_kwargs)
    else:
        return post_kwargs 


    if registration.status_code == 200:
        return {
            "status": "success",
            "message": f"Uploader '{kwargs['uploader_id']}' register successfully",
            "content": payload
        }, 200


    nokmsg = f"Could not register uploader '{kwargs['uploader_id']}'"
    log.error(nokmsg)
    return {"status": "fail", "message": nokmsg, "content": payload}, 400






