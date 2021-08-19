import requests
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.decorators.auth_decorators import authenticated_machine
# TODO from app.licenseware.common.validators.registry_payload_validators import validate_register_app_payload




@authenticated_machine
def register_report(**kwargs):
    
    if not envs.app_is_authenticated():
        log.warning('App not registered, no auth token available')
        return {
            "status": "fail",
            "message": "App not registered, no auth token available"
        }, 401
    

    payload = {
        'data': [{
            "app_id": envs.APP_ID,
            "report_id": kwargs['id'],
            "report_name": kwargs['name'],
            "description": kwargs['description'],
            "flags": kwargs['flags'],
            "url": kwargs['url'], #TODO f'{os.getenv("APP_BASE_PATH")}{os.getenv("APP_URL_PREFIX")}/reports{self.url}',
            "refresh_registry_url": kwargs['refresh_registry_url'],
            "connected_apps": kwargs['connected_apps']
        }]
    }
    
    
    # log.info(payload)    
    # TODO validate_register_app_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_REPORT_URL, json=payload, headers=headers)
    
    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['name']}"
        log.error(nokmsg)
        return { "status": "fail", "message": nokmsg }, 500
    
    return {
        "status": "success",
        "message": f"Report {kwargs['name']} registered successfully"
    }, 200

    