from typing import List

from flask import Request

from licenseware.common.constants.envs import envs
from licenseware.registry_service import register_report
from licenseware.report_components import BaseReportComponent
from licenseware.report_components.build_match_expression import condition_switcher
from licenseware.report_snapshot import ReportSnapshot
from licenseware.tenants import get_tenants_with_public_reports
from licenseware.utils.tokens import delete_public_token, get_public_token


class ReportBuilder:
    """

    :name - report name
    :report_id - report id (will be used to construct path/route)
    :description - report data description
    :report_components - instantiated class objects from report_components
    :registrable - If True report will be registered to registry service
    :report_path - the endpoint/route on which this report is found
    :preview_image - the image name from resources folder. If not provided it will look for an image with the name `report_id.png`
    :preview_image_dark - the dark theme image name from resources folder. If not provided it will look for an image with the name `report_id_dark.png`
    :connected_apps - related apps which are needed to build this report
    :flags - use flags dataclass from licenseware.commun.constants


    """

    def __init__(
        self,
        name: str,
        report_id: str,
        description: str,
        report_components: list,
        registrable: bool = True,
        report_path: str = None,
        preview_image: str = None,
        preview_image_dark: str = None,
        connected_apps: list = [],
        flags: list = [],
        filters: list = [],
    ):

        if envs.DEPLOYMENT_SUFFIX is not None:
            name = name + envs.DEPLOYMENT_SUFFIX
            report_id = report_id + envs.DEPLOYMENT_SUFFIX

        self.report_id = report_id
        self.name = name
        self.description = description
        self.components: List[BaseReportComponent] = report_components
        self.report_path = report_path or "/" + report_id
        self.public_report_path = self.report_path + "/public"
        self.register_report_path = self.report_path + "/register"
        self.registrable = registrable
        self.connected_apps = connected_apps
        self.app_id = envs.APP_ID
        self.flags = flags

        self.url = envs.REPORT_URL + self.report_path
        self.snapshot_url = envs.REPORT_URL + self.report_path + "/snapshot"
        self.public_url = envs.REPORT_URL + self.public_report_path
        self.ui_public_url = envs.FRONTEND_URL + envs.REPORT_PATH + "/public"
        self.preview_image_path = self.report_path + "/preview_image"
        self.preview_image_dark_path = self.report_path + "/preview_image_dark"
        self.preview_image_url = envs.REPORT_URL + self.preview_image_path
        self.preview_image_dark_url = envs.REPORT_URL + self.preview_image_dark_path
        self.preview_image = preview_image
        self.preview_image_dark = preview_image_dark
        self.public_for_tenants = get_tenants_with_public_reports(
            report_id=self.report_id
        )

        # Needed to overwrite report_components and filters
        self.report_components = []
        self.filters = filters
        self.register_components()

        self.reportvars = vars(self)

    def return_json_payload(self):
        payload = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "name": self.name,
            "description": self.description,
            "flags": self.flags,
            "report_components": self.report_components,
            "filters": self.filters,
            "url": self.url,
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "public_for_tenants": get_tenants_with_public_reports(
                report_id=self.report_id
            ),
            "preview_image_url": self.preview_image_url,
            "preview_image_dark_url": self.preview_image_dark_url,
            "connected_apps": self.connected_apps,
        }
        return payload, 200

    def get_report_public_url(self, flask_request: Request):
        tenant_id = flask_request.headers.get("TenantId")
        expire = flask_request.args.get("expire")
        expire = 90 if expire is None else int(expire)
        token = get_public_token(
            tenant_id, expire, self.report_id, self.ui_public_url, self.public_url
        )
        return self.ui_public_url + "?public_token=" + token

    def delete_report_public_url(self, flask_request: Request):
        tenant_id = flask_request.headers.get("TenantId")
        return delete_public_token(tenant_id, self.report_id)

    def get_snapshot_version(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.get_snapshot_version()

    def get_available_versions(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.get_available_versions()

    def get_snapshot_metadata(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.get_snapshot_metadata()

    def get_snapshot_component(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.get_snapshot_component()

    def update_snapshot(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.update_snapshot()

    def delete_snapshot(self, flask_request: Request):
        rs = ReportSnapshot(self, flask_request)
        return rs.delete_snapshot()

    def register_report(self):
        return register_report(
            **{
                **self.reportvars,
                **{
                    "public_for_tenants": get_tenants_with_public_reports(
                        report_id=self.report_id
                    )
                },
            }
        )

    def register_components(self):

        for order, component in enumerate(self.components):
            for registered_component in self.report_components:
                if registered_component["component_id"] == component.component_id:
                    raise Exception(
                        f"Component id '{component.component_id}' was already declared"
                    )

            metadata = component.get_registration_payload()

            metadata["order"] = metadata["order"] or order + 1
            metadata["url"] = self.url + metadata.pop("path")
            metadata["type"] = metadata.pop("component_type")

            self.report_components.append(metadata)

    def register_filters(self, filters: list):
        self.filters.extend(filters)

    @classmethod  # same func as in base_report_component
    def build_filter(
        cls,
        column: str,
        allowed_filters: list,
        visible_name: str,
        validate: bool = True,
    ):
        """
        Will return a dictionary similar to the one bellow:

        {
            "column": "version.edition",
            "allowed_filters": [
                "equals", "contains", "in_list"
            ],
            "visible_name": "Product Edition"
        }

        The dictionary build will be used to filter mongo

        """

        if validate:

            if " " in column:
                raise ValueError(
                    "Parameter `column` can't contain spaces and must be all lowercase like `device_name`"
                )

            for f in allowed_filters:
                if f not in condition_switcher.keys():
                    raise ValueError(f"Filter {f} not in {condition_switcher.keys()}")

        return dict(
            column=column, allowed_filters=allowed_filters, visible_name=visible_name
        )
