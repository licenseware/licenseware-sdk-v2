import requests
import traceback
import os

from licenseware.utils.logger import log

REGISTRY_SERVICE_URL = os.getenv("REGISTRY_SERVICE_URL")

class ExternalDataService:

    @staticmethod
    def _get_registry_service_data(headers, endpoint):
        try:
            reg_data = requests.get(
                url=f"{REGISTRY_SERVICE_URL}/{endpoint}",
                headers=headers
            )
            return reg_data.json()
        except Exception:
            log.error(traceback.format_exc())
            return [{
                'data': []
            }]   


    @staticmethod
    def _get_component_url(components, app_id, component_id):
        try:
            return [d['url'] for d in components['data'] if d['app_id'] == app_id and d['component_id'] == component_id][0]
        except IndexError:
            log.error(traceback.format_exc())
            return False


    @staticmethod
    def get_data(_request, app_id, component_id, filter_payload=None):
        try:
            headers = {
                "TenantId": _request.headers.get("TenantId"),
                "Authorization": _request.headers.get("Authorization"),
            }
            
            registry_service_components = ExternalDataService._get_registry_service_data(headers, "components")
            service_url = ExternalDataService._get_component_url(
                components=registry_service_components,
                app_id=app_id,
                component_id=component_id
            )
            if not service_url:
                return []

            if filter_payload:
                data = requests.post(
                    url=service_url, headers=headers, json=filter_payload
                )
            else:
                data = requests.get(url=service_url, headers=headers)
                
            if data.status_code == 200:
                return data.json()
            else:
                log.warning(f"Could not retrieve data for {component_id} from {app_id}")
                log.warning(f"GET {service_url} {data.status_code}")
                return []
        except Exception:
            log.error(traceback.format_exc())
            return False

    @staticmethod
    def _get_uploader_url(uploaders, app_id, uploader_id):
        try:
            return [d['upload_url'] for d in uploaders['data'] if d['app_id'] == app_id and d['uploader_id'] == uploader_id][0]
        except IndexError:
            log.error(traceback.format_exc())
            return False
    
    @staticmethod
    def get_upload_url(_request, app_id, uploader_id):
        headers = {
            "TenantId": _request.headers.get("TenantId"),
            "Authorization": _request.headers.get("Authorization"),
        }
        registry_service_uploaders = ExternalDataService._get_registry_service_data(headers, "uploaders")

        upload_url = ExternalDataService._get_uploader_url(
            uploaders=registry_service_uploaders, 
            app_id=app_id, 
            uploader_id=uploader_id
            )
        
        if not upload_url:
            return None
        
        return upload_url

