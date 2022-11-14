import os
import traceback
from dataclasses import dataclass, fields, is_dataclass
from typing import Union

import requests
from flask import Request

from licenseware.auth import Authenticator
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import get_flask_request_dict
from licenseware.utils.tokens import get_public_token_data


class ExternalDataService:
    """
    Dependencies:
      - service urls defined in the env vars
      - app service urls loaded from env vars, naming convention APP_SERVICE_URL -> i.e IFMP_SERVICE_URL, MDM_SERVICE_URL
      - local application envs created in app/config.py, see mdm-service/app/config.py
    Usage:
      - Pulling data from external components
       ```py
        from app.config import envs as app_envs
        external_data = ExternalDataService(app_envs=app_envs).get_data(
            _request=flask_request,
            app_id="ifmp-service",
            component_id="devices_by_type",
            filter_payload=[filter_payload]
        )
       ```
      - Creating the upload url for external uploader
       ```py
        from app.config import envs as app_envs
        upload_url = ExternalDataService(app_envs=app_envs).get_upload_url(
            app_id="ifmp-service",
            uploader_id="cpuq"
        )
       ```
    """

    def __init__(self, app_envs: dataclass):
        self.envs = self.validate_envs(app_envs)
        self.service_urls = self.map_service_urls()

    def validate_envs(self, envs: dataclass):
        assert (
            is_dataclass(envs) == True
        ), "Please init with env vars in a dataclass, see licenseware.common.constants.envs"
        return envs

    def map_service_urls(self) -> dict:
        """
        Find service urls in env vars and create a map by app_id, ignores auth and registry service.
        Output looks like:
        {
            "ifmp-service": "http://host/ifmp-service"
        }

        """
        url_map = {}
        for field in fields(self.envs):
            env_var = field.name.lower()
            if any(excluded in env_var for excluded in ["auth", "registry"]):
                continue
            if "service_url" in env_var:
                url_map.update(
                    {
                        env_var.replace("_service_url", "-service"): getattr(
                            self.envs, field.name
                        )
                    }
                )
        return url_map

    def deserialize_request(self, flask_request: Union[Request, dict]) -> dict:
        if isinstance(flask_request, dict):
            return flask_request
        if isinstance(flask_request, Request):
            return get_flask_request_dict(flask_request)
        return dict()

    def _get_headers(self, _request: Union[Request, dict]) -> dict:

        deserialized_request = self.deserialize_request(_request)
        public_token = deserialized_request.get("public_token", None)
        if public_token:
            # Saving some `trips` to auth
            Authenticator.connect()

            data = get_public_token_data(public_token)
            headers = {
                "TenantId": data["tenant_id"],
                "Authorization": os.getenv("AUTH_TOKEN"),
            }
            return headers
        headers = {
            "TenantId": deserialized_request.get(
                "TenantId", deserialized_request.get("Tenantid")
            ),
            "Authorization": deserialized_request.get("Authorization"),
        }
        return headers

    def get_component_url(self, app_id: str, component_id: str) -> str:
        try:
            return f"{self.service_urls[app_id]}/report-components/{component_id}"
        except KeyError:
            log.error(
                f"Couldn't create external component url from: {self.service_urls}"
            )
            return None

    def get_data(
        self, _request, app_id: str, component_id: str, filter_payload: dict = None
    ) -> list:
        try:

            headers = self._get_headers(_request)
            service_url = self.get_component_url(
                app_id=app_id, component_id=component_id
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
                log.warning(f"GET [{data.status_code}] {service_url} ")
                return []
        except Exception:
            log.error(traceback.format_exc())
            return False

    def get_upload_url(self, app_id: str, uploader_id: str) -> str:
        try:
            return f"{self.service_urls[app_id]}/uploads/{uploader_id}/files"
        except KeyError:
            log.error(f"Couldn't create external upload url from: {self.service_urls}")
            return None
