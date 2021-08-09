"""

Register an app to registry service


from licenseware import AppDefinition

app_definition = AppDefinition(
    id="new-service",
    name="Short expresive name",
    description="long description",
    icon="default.png",
    app_activation_url='/app/init'
    activated_tenants_func=get_activated_tenants,
    tenants_with_data_func=get_tenants_with_data,
)

app_definition.register_app()

Where:
- get_activated_tenants : returns a list of tenants ids which have quota initialized
- get_tenants_with_data : returns a list of dicts where each dict has tenantid, last_update_date fields 
which represents that tenant has processed files and has saved data as a result 

"""

import os
import requests
from licenseware.utils.urls import BASE_URL, REGISTRY_SERVICE_URL
from licenseware.utils.log_config import log
from licenseware.decorators.auth_decorators import authenticated_machine



class AppDefinition:

    def __init__(
        self, 
        id, 
        name, 
        description,
        activated_tenants_func,
        tenants_with_data_func,
        flags=[],
        icon="default.png", 
        app_activation_url='/app/init',
        refresh_registration_url='/register_all',
        editable_tables_url='/editable_tables',
        history_report_url='/reports/history_report',
        tenant_registration_url='/tenant_registration_url'
    ):

        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.flags = flags
        self.activated_tenants_func = activated_tenants_func
        self.tenants_with_data_func = tenants_with_data_func
        self.app_activation_url = app_activation_url
        self.refresh_registration_url = refresh_registration_url
        self.editable_tables_url = editable_tables_url
        self.history_report_url = history_report_url
        self.tenant_registration_url = tenant_registration_url
        

    @authenticated_machine
    def register_app(self):
        
        if os.getenv('APP_AUTHENTICATED') != 'true':
            log.warning('App not registered, no auth token available')
            return {
                "status": "fail",
                "message": "App not registered, no auth token available"
            }, 401

        payload = {
            'data': [{
                "app_id": self.id,
                "name": self.name,
                "tenants_with_app_activated": self.activated_tenants_func(),
                "tenants_with_data_available": self.tenants_with_data_func(),
                "description": self.description,
                "flags": self.flags,
                "icon": self.icon,
                "refresh_registration_url": BASE_URL + self.refresh_registration_url,
                "app_activation_url": BASE_URL + self.app_activation_url,
                "editable_tables_url": BASE_URL + self.editable_tables_url,
                "history_report_url":  BASE_URL + self.history_report_url,
                "tenant_registration_url":  BASE_URL + self.tenant_registration_url
            }]
        }

        log.info(payload)
        
        url = REGISTRY_SERVICE_URL + '/apps'
        headers = {"Authorization": os.getenv('AUTH_TOKEN')}
        registration = requests.post(url, json=payload, headers=headers)
        
        if registration.status_code != 200:
            log.warning(f"Could not register app {self.name}")
            return { "status": "fail", "message": "Could not register app" }, 500
        
        return {"status": "success","message": "App registered successfully"}, 200

    @authenticated_machine
    def register_all(self, reports=[], uploaders=[]):
        try:
            self.register_app()
            [r.register_report() for r in reports]
            [u.register_uploader() for u in uploaders]
            return True
        except:
            log.exception("Failed to register_all")
            return False
