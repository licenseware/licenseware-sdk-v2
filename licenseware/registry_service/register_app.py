import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.tenants import get_activated_tenants, get_tenants_with_data
from licenseware.common.validators.registry_payload_validators import validate_register_app_payload


@authenticated_machine
def register_app(**kwargs):
    """
        Send a post request to registry service to make app available in front-end
    """

    payload = {
        'data': [{
            "app_id": kwargs['app_id'],
            "name": kwargs['name'],
            "tenants_with_app_activated": get_activated_tenants(),
            "tenants_with_data_available": get_tenants_with_data(),
            "description": kwargs['description'],
            "flags": kwargs['flags'],
            "icon": kwargs['icon'],
            "features_url": kwargs['features_url'],
            "features": [f.get_details() for f in kwargs['features']],
            "refresh_registration_url": kwargs['refresh_registration_url'],
            "app_activation_url": kwargs['app_activation_url'],
            "editable_tables_url": kwargs['editable_tables_url'],
            "history_report_url": kwargs['history_report_url'],
            "tenant_registration_url": kwargs['tenant_registration_url'],
            "terms_and_conditions_url": kwargs['terms_and_conditions_url'],
            "app_meta": kwargs['app_meta']
        }]
    }

    log.info(payload)
    # validate_register_app_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    registration = requests.post(url=envs.REGISTER_APP_URL, json=payload, headers=headers)

    if registration.status_code != 200:
        nokmsg = f"Could not register app {kwargs['name']}"
        log.error(nokmsg)
        return {"status": "fail", "message": nokmsg, "content": payload}, 500

    return {
               "status": "success",
               "message": f"App {kwargs['name']} registered successfully",
               "content": payload
           }, 200
