import requests
import traceback
import os

from licenseware.utils.logger import log


class ExternalDataService:
    @staticmethod
    def _get_all_components(headers):
        registry_service_url = os.get("REGISTRY_SERVICE_URL")
        try:
            comp_data = requests.get(
                url=f"{registry_service_url}/components"
            )
            return comp_data.json()
        except Exception:
            log.error(traceback.format_exc())


    @staticmethod
    def _get_component_url(components, app_id, component_id):
        return [d['url'] for d in components if d['app_id'] == app_id and d['component_id'] == component_id][0]


    @staticmethod
    def get_data(_request, app_id, component_id, filter_payload=None):
        try:
            headers = {
                "TenantId": _request.headers.get("TenantId"),
                "Authorization": _request.headers.get("Authorization"),
            }
            
            registry_service_components = ExternalDataService._get_all_components(headers)
            service_url = ExternalDataService._get_component_url(
                components=registry_service_components,
                app_id=app_id,
                component_id=component_id
            )

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