import requests
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
from app.licenseware.common.validators.registry_payload_validators import validate_register_report_component_payload




@authenticated_machine
def register_component(**kwargs):
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
    
    
    app_id = envs.APP_ID + envs.PERSONAL_SUFFIX if envs.environment_is_local() else envs.APP_ID
    component_id = kwargs['component_id'] + envs.PERSONAL_SUFFIX if envs.environment_is_local() else kwargs['component_id']
    
    payload = {
        'data': [{
            "app_id": app_id,
            "component_id": component_id,
            "url": kwargs['url'],
            "order": kwargs['order'],
            "style_attributes": kwargs['style_attributes'],
            "attributes": kwargs['attributes'],
            "title": kwargs['title'],
            "type": kwargs['component_type'],
            "filters": kwargs['filters']
            
        }]
    }

    log.info(payload)    
    validate_register_report_component_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_REPORT_COMPONENT_URL, json=payload, headers=headers)
    
    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['component_id']}"
        log.error(nokmsg)
        return { "status": "fail", "message": nokmsg, "content": payload }, 500
    
    return {
        "status": "success",
        "message": f"Report {kwargs['component_id']} registered successfully",
        "content": payload
    }, 200

    