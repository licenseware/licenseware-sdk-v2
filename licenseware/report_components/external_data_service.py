import os
import traceback

import requests

from licenseware.auth import Authenticator
from licenseware.utils.logger import log
from licenseware.utils.tokens import get_public_token_data

REGISTRY_SERVICE_URL = os.getenv("REGISTRY_SERVICE_URL")


class ExternalDataService:
    @staticmethod
    def _get_headers(_request):

        public_token = _request.args.get("public_token")

        if public_token is not None:
            # Saving some `trips` to auth
            Authenticator.connect()

            data = get_public_token_data(public_token)

            headers = {
                "TenantId": data["tenant_id"],
                "Authorization": os.getenv("AUTH_TOKEN"),
            }

        else:
            headers = {
                "TenantId": _request.headers.get("TenantId"),
                "Authorization": _request.headers.get("Authorization"),
            }

        return headers

    @staticmethod
    def _get_registry_service_data(headers: dict, endpoint: str) -> list:
        """
        If the tenant check fails, it tries the machine check.

        Machine check is handled by the caller, passing env token.
        """
        try:
            # Try both tenant check and if that fails try machine check
            reg_data = requests.get(
                url=f"{REGISTRY_SERVICE_URL}/{endpoint}", headers=headers
            )
            if reg_data.status_code != 200:
                log.info(
                    "Couldn't get registry service data with tenant auth, fallback to machine auth"
                )
                reg_data = requests.get(
                    url=f"{REGISTRY_SERVICE_URL}/v1/{endpoint}",
                    headers={"Authorization": headers["Authorization"]},
                )
                return reg_data.json()
            return reg_data.json()
        except Exception:
            log.error(traceback.format_exc())
            return [{"data": []}]

    @staticmethod
    def _get_component_url(components: dict, app_id: str, component_id: str) -> str:
        try:
            return [
                d["url"]
                for d in components["data"]
                if d["app_id"] == app_id and d["component_id"] == component_id
            ][0]
        except IndexError:
            log.error(traceback.format_exc())
            return False

    @staticmethod
    def get_data(
        _request, app_id: str, component_id: str, filter_payload: dict = None
    ) -> list:
        try:

            headers = ExternalDataService._get_headers(_request)

            registry_service_components = (
                ExternalDataService._get_registry_service_data(headers, "components")
            )
            service_url = ExternalDataService._get_component_url(
                components=registry_service_components,
                app_id=app_id,
                component_id=component_id,
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
    def _get_uploader_url(uploaders: dict, app_id: str, uploader_id: str) -> str:
        try:
            return [
                d["upload_url"]
                for d in uploaders["data"]
                if d["app_id"] == app_id and d["uploader_id"] == uploader_id
            ][0]
        except IndexError:
            log.error(traceback.format_exc())
            return False

    @staticmethod
    def get_upload_url(_request: dict, app_id: str, uploader_id: str) -> str:
        headers = {
            "TenantId": _request.get("Tenantid"),
            "Authorization": _request.get("Authorization"),
        }
        registry_service_uploaders = ExternalDataService._get_registry_service_data(
            headers, "uploaders"
        )

        upload_url = ExternalDataService._get_uploader_url(
            uploaders=registry_service_uploaders, app_id=app_id, uploader_id=uploader_id
        )

        if not upload_url:
            return None

        return upload_url
