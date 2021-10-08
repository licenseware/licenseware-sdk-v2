import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.common.validators.registry_payload_validators import validate_register_report_payload




@authenticated_machine
def register_report(get_kwargs=False, **kwargs):
    
    if kwargs['registrable'] is False: 
        return {
            "status": "success",
            "message": f"Report {kwargs['name']} will not be registered to registry-service (registrable is set to False)",
            "content": None
        }, 200
    
        
    app_id = envs.APP_ID + envs.PERSONAL_SUFFIX if envs.environment_is_local() else envs.APP_ID
    report_id = kwargs['report_id'] + envs.PERSONAL_SUFFIX if envs.environment_is_local() else kwargs['report_id']
    
    payload = {
        'data': [{
            "app_id": app_id,
            "report_id": report_id,
            "report_name": kwargs['name'],
            "description": kwargs['description'],
            "flags": kwargs['flags'],
            "url": kwargs['url'],
            # TODO update registry service
            # "preview_image_url":kwargs['preview_image_url'],
            # "report_components":  kwargs['report_components'],
            "connected_apps": kwargs['connected_apps'],
            # "filters" : kwargs['filters']
        }]
    }
    
    
    if get_kwargs == False: log.info(payload)    
    validate_register_report_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    post_kwargs = dict(url=envs.REGISTER_REPORT_URL, json=payload, headers=headers)
    
    if get_kwargs: return post_kwargs
    
    
    registration = requests.post(**post_kwargs)
    
    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['name']}"
        log.error(nokmsg)
        return { "status": "fail", "message": nokmsg, "content": payload }, 500
    
    return {
        "status": "success",
        "message": f"Report {kwargs['name']} registered successfully",
        "content": payload
    }, 200

    