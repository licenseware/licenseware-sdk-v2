import requests
from licenseware.utils.logger import log


class ExternalDataService:
    @staticmethod
    def get_data(_request, app_id, component_id, filter_payload=None):
        try:
            service_url = f"http://kong/{app_id}/report-components/{component_id}"
            headers = {
                "TenantId": _request.headers.get("TenantId"),
                "Authorization": _request.headers.get("Authorization"),
            }
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
        except Exception as e:
            log.exception(str(e))
            return False