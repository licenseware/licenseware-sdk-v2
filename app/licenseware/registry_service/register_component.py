import requests
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
# TODO from app.licenseware.common.validators.registry_payload_validators import validate_register_report_payload




@authenticated_machine
def register_component(**kwargs):
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
    

    payload = {
        'data': [{
            "app_id": envs.APP_ID,
            "component_id": kwargs['component_id'],
            "component_url": kwargs['component_url'],
            "order": kwargs['order'],
            "style_attributes": kwargs['style_attributes'],
            "attributes": kwargs['attributes'],
            "title": kwargs['title'],
            "type": kwargs['component_type']
        }]
    }

    log.info(payload)    
    # TODO validate_register_report_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_REPORT_COMPONENT_URL, json=payload, headers=headers)
    
    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['name']}"
        log.error(nokmsg)
        return { "status": "fail", "message": nokmsg, "content": payload }, 500
    
    return {
        "status": "success",
        "message": f"Report {kwargs['name']} registered successfully",
        "content": payload
    }, 200

    