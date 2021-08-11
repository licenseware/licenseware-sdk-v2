import requests
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
from app.licenseware.common.validators import validate_register_app_payload




@authenticated_machine
def register_app(**kwargs):
    """
        Send a post request to registry service to make app available in front-end
    """
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
        
    full_url = lambda url: envs.BASE_URL + url

    payload = {
        'data': [{
            "app_id": kwargs['id'],
            "name": kwargs['name'],
            "tenants_with_app_activated": kwargs['activated_tenants'],
            "tenants_with_data_available": kwargs['tenants_with_data'],
            "description": kwargs['description'],
            "flags": kwargs['flags'],
            "icon": kwargs['icon'],
            "refresh_registration_url":  full_url(kwargs['refresh_registration_url']),
            "app_activation_url": full_url(kwargs['app_activation_url']),
            "editable_tables_url": full_url(kwargs['editable_tables_url']),
            "history_report_url":  full_url(kwargs['history_report_url']),
            "tenant_registration_url":  full_url(kwargs['tenant_registration_url'])
        }]
    }
    
    validate_register_app_payload(payload)

    log.info(payload)
    
    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_APP_URL, json=payload, headers=headers)
    
    if registration.status_code != 200:
        nok_msg = f"Could not register app {kwargs['name']}"
        log.error(nok_msg)
        return { "status": "fail", "message": nok_msg }, 500
    
    return {
        "status": "success",
        "message": f"App {kwargs['name']} registered successfully"
    }, 200
