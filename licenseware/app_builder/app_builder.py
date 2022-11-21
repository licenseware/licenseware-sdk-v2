"""

`AppBuilder` is reponsible for creating the Api from the `X_namespace` packages and `X_route` modules. Authenticates the `App` and sends the registration information to registry-service. 

Notice that history report route/path is provided but is not implemented that's because a report must be defined with aggregated data from AnalysisStats mongo collection. 

"""

from dataclasses import dataclass
from typing import Callable, Dict, List

from flask import Flask
from flask_restx import Api, Namespace, Resource
from marshmallow.schema import Schema

from licenseware.app_builder.app_activation_route import add_app_activation_route
from licenseware.app_builder.app_registration_route import add_app_registration_route
from licenseware.app_builder.data_sync_namespace import (
    data_sync_namespace,
    get_data_sync_namespace,
)
from licenseware.app_builder.download_as_route import add_download_as_route
from licenseware.app_builder.editable_tables_route import add_editable_tables_route
from licenseware.app_builder.endpoint_builder_namespace import (
    endpoint_builder_namespace,
)
from licenseware.app_builder.features_namespace import (
    features_namespace,
    get_features_namespace,
)
from licenseware.app_builder.features_route import add_features_route
from licenseware.app_builder.refresh_registration_route import (
    add_refresh_registration_route,
)
from licenseware.app_builder.report_components_namespace import (
    get_report_individual_components_namespace,
    report_components_namespace,
)
from licenseware.app_builder.reports_namespace import (
    get_public_report_components_namespace,
    get_public_report_metadata_namespace,
    get_report_components_namespace,
    get_report_image_preview_dark_namespace,
    get_report_image_preview_namespace,
    get_report_metadata_namespace,
    get_report_register_namespace,
    get_report_snapshot_namespace,
    reports_namespace,
)
from licenseware.app_builder.reprocess_data_route import add_reprocess_data_route
from licenseware.app_builder.tenant_registration_route import (
    add_tenant_registration_route,
)
from licenseware.app_builder.terms_and_conditions_route import (
    add_terms_and_conditions_route,
)
from licenseware.app_builder.uploads_namespace import (
    get_filenames_validation_namespace,
    get_filestream_validation_namespace,
    get_quota_namespace,
    get_status_namespace,
    uploads_namespace,
)
from licenseware.auth import Authenticator
from licenseware.common.constants.envs import envs
from licenseware.common.validators.validate_integration_details import (
    validate_integration_details,
)
from licenseware.decorators.xss_decorator import xss_before_request
from licenseware.editable_table import EditableTable
from licenseware.feature_builder import FeatureBuilder
from licenseware.mongodata import create_collection
from licenseware.registry_service import register_all
from licenseware.report_builder.report_builder import ReportBuilder
from licenseware.report_components.base_report_component import BaseReportComponent
from licenseware.schema_namespace import SchemaNamespace
from licenseware.tenants import (
    get_activated_tenants,
    get_tenants_with_data,
    get_tenants_with_public_reports,
)
from licenseware.uploader_builder.uploader_builder import UploaderBuilder
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import swagger_authorization_header

# from .decrypt_namespace import decrypt_namespace
# from .decrypt_namespace import get_decrypt_namespace


@dataclass
class base_paths:
    app_activation_path: str = "/activate_app"
    register_app_path: str = "/register_app"
    refresh_registration_path: str = "/refresh_registration"
    editable_tables_path: str = "/editable_tables"
    history_report_path: str = "/reports/history_report"
    tenant_registration_path: str = "/register_tenant"
    terms_and_conditions_path: str = "/terms_and_conditions"
    features_path: str = "/features"
    data_sync_path: str = "/data-sync"
    reprocess_data_path: str = "/reprocess-data"


class AppBuilder:
    def __init__(
        self,
        name: str,
        description: str,
        flags: list = None,
        app_meta: dict = None,
        features: List[FeatureBuilder] = None,
        editable_tables: List[EditableTable] = None,
        editable_tables_schemas: List[Schema] = None,
        data_sync_schema: Schema = None,
        broker_funcs: Dict[str, List[Callable]] = None,
        doc_authorizations: dict = swagger_authorization_header,
        api_decorators: list = None,
        integration_details: List[dict] = None,
        icon: str = "default.png",
        registrable: bool = True,
        **options,
    ):

        self.name = name
        self.app_id = envs.APP_ID
        self.registrable = registrable

        if envs.DEPLOYMENT_SUFFIX is not None:
            self.name = self.name + envs.DEPLOYMENT_SUFFIX
            self.app_id = self.app_id + envs.DEPLOYMENT_SUFFIX

        self.description = description
        self.flags = flags or []
        self.app_meta = app_meta
        self.features = features or []
        self.data_sync_schema = data_sync_schema
        self.editable_tables = editable_tables or []
        self.editable_tables_schemas = editable_tables_schemas or []
        self.broker_funcs = broker_funcs
        self.icon = icon

        if integration_details is not None:
            validate_integration_details(integration_details)

        self.integration_details = integration_details

        self.app_activation_path = base_paths.app_activation_path
        self.register_app_path = base_paths.register_app_path
        self.refresh_registration_path = base_paths.refresh_registration_path
        self.editable_tables_path = base_paths.editable_tables_path
        self.history_report_path = base_paths.history_report_path
        self.tenant_registration_path = base_paths.tenant_registration_path
        self.terms_and_conditions_path = base_paths.terms_and_conditions_path
        self.features_path = base_paths.features_path
        self.data_sync_path = base_paths.data_sync_path
        self.reprocess_data_path = base_paths.reprocess_data_path

        self.app_activation_url = envs.BASE_URL + self.app_activation_path
        self.refresh_registration_url = envs.BASE_URL + self.refresh_registration_path
        self.editable_tables_url = envs.BASE_URL + self.editable_tables_path
        self.history_report_url = envs.BASE_URL + self.history_report_path
        self.tenant_registration_url = envs.BASE_URL + self.tenant_registration_path
        self.terms_and_conditions_url = envs.BASE_URL + self.terms_and_conditions_path
        self.features_url = envs.BASE_URL + self.features_path
        self.data_sync_url = envs.BASE_URL + self.data_sync_path
        self.reproces_data_url = envs.BASE_URL + self.reprocess_data_path

        self.authorizations = doc_authorizations
        self.decorators = [] if api_decorators is None else api_decorators

        # parameters with default values provided can be added stright to __init__
        # otherwise added them to options until apps are actualized
        self.options = options

        # TODO version needs to be added to all urls + '/v' + self.version
        self.prefix = envs.APP_PATH
        self.app = None
        self.api = None
        self.ns = None
        self.reports: List[ReportBuilder] = []
        self.report_components: List[BaseReportComponent] = []
        self.uploaders: List[UploaderBuilder] = []
        self.custom_namespaces: List[Namespace] = []

        self.appvars = vars(self)

    def init_app(self, app: Flask, register: bool = False):

        if envs.PROMETHEUS_ENABLED:
            from prometheus_flask_exporter import PrometheusMetrics

            metrics = PrometheusMetrics(app)

            @app.route(envs.METRICS_URI)
            def metrics():
                return metrics()

        # This hides flask_restx `X-fields` from swagger headers
        app.config["RESTX_MASK_SWAGGER"] = False
        app.before_request(xss_before_request)

        @app.after_request
        def after_request(response):
            response.headers.set("Access-Control-Allow-Origin", "*")
            response.headers.set(
                "Access-Control-Allow-Headers",
                "Content-Type,Authorization,TenantId,Tenantid",
            )
            response.headers.set(
                "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
            )
            response.headers.set("Access-Control-Allow-Credentials", "true")

            # https://flask.palletsprojects.com/en/2.1.x/security/#security-csp
            # XSS
            response.headers["X-Content-Type-Options"] = "nosniff"

            return response

        self.app = app

        if not self.uploaders:
            log.warning("No uploaders provided")
        if not self.reports:
            log.warning("No reports provided")

        self.authenticate_app()
        self.init_api()
        self.init_routes()
        self.init_namespaces()
        self.init_broker()
        if register:
            self.register_app()

        return self.app

    def init_broker(self, app: Flask = None):
        self.broker = broker.init_app(app or self.app)
        return self.broker

    def authenticate_app(self):

        if envs.DESKTOP_ENVIRONMENT:
            return

        response, status_code = Authenticator.connect(
            max_retries="infinite", wait_seconds=2
        )
        if status_code != 200:
            raise Exception("App failed to authenticate!")
        log.info("Authentification succeded!")
        return response, status_code

    def init_api(self):

        self.api = Api(
            app=self.app,
            title=self.name,
            description=self.description,
            prefix=self.prefix,
            default=self.name,
            default_label=self.description,
            decorators=self.decorators,
            authorizations=self.authorizations,
            security=list(self.authorizations.keys()),
            doc=self.prefix + "/docs",
        )

    def init_routes(self):

        # Here we are adding the routes available for each app
        # Api must be passed from route function back to this context
        api_funcs = [
            add_refresh_registration_route,
            add_editable_tables_route,
            add_tenant_registration_route,
            add_app_activation_route,
            add_app_registration_route,
            add_terms_and_conditions_route,
            add_download_as_route,
            add_features_route,
            add_reprocess_data_route,
        ]

        for func in api_funcs:
            if func.__name__ == "add_refresh_registration_route":
                self.api = func(self.api, self)
            else:
                self.api = func(self.api, self.appvars)

        # Another way is to group routes in namespaces
        # This way the url prefix is specified only in the namespace
        self.add_uploads_routes()
        self.add_reports_routes()
        self.add_report_components_routes()
        self.add_editables_routes()
        self.add_features_routes()
        self.add_data_sync_routes()
        # self.add_decrypt_routes()

    def add_uploads_routes(self):

        ns_funcs = [
            get_filenames_validation_namespace,
            get_filestream_validation_namespace,
            get_status_namespace,
            get_quota_namespace,
        ]

        for func in ns_funcs:
            self.register_namespace(
                func(ns=uploads_namespace, uploaders=self.uploaders)
            )

    def add_reports_routes(self):

        ns_funcs = [
            get_report_register_namespace,
            get_report_metadata_namespace,
            get_report_components_namespace,
            get_report_image_preview_namespace,
            get_report_image_preview_dark_namespace,
            get_report_snapshot_namespace,
            get_public_report_metadata_namespace,
            get_public_report_components_namespace,
        ]

        for func in ns_funcs:
            self.register_namespace(func(ns=reports_namespace, reports=self.reports))

    def add_report_components_routes(self):

        ns_funcs = [get_report_individual_components_namespace]

        for func in ns_funcs:
            self.register_namespace(
                func(
                    ns=report_components_namespace,
                    report_components=self.report_components,
                )
            )

    def add_editables_routes(self):

        for editable in self.editable_tables:
            if editable.namespace:
                self.register_namespace(editable.namespace)
            else:
                ns = SchemaNamespace(schema=editable.schema).initialize()
                self.register_namespace(ns)

    def add_features_routes(self):

        ns_funcs = [get_features_namespace]

        for func in ns_funcs:
            self.register_namespace(func(ns=features_namespace, features=self.features))

    def add_data_sync_routes(self):

        if self.data_sync_schema is None:
            return

        ns_funcs = [get_data_sync_namespace]

        for func in ns_funcs:
            self.register_namespace(
                func(ns=data_sync_namespace, data_sync_schema=self.data_sync_schema)
            )

    # def add_decrypt_routes(self):

    #     ns_funcs = [get_decrypt_namespace]

    #     for func in ns_funcs:
    #         self.register_namespace(
    #             func(ns=decrypt_namespace)
    #         )

    def get_serialized_app_dict(self):

        app_dict = {
            k: v
            for k, v in self.appvars.items()
            if k
            in [
                "app_id",
                "name",
                "description",
                "flags",
                "icon",
                "refresh_registration_url",
                "app_activation_url",
                "editable_tables_url",
                "history_report_url",
                "tenant_registration_url",
                "terms_and_conditions_url",
                "features_url",
                "app_meta",
                "integration_details",
            ]
        }

        app_dict["features"] = [f.get_details() for f in self.features]
        app_dict["tenants_with_app_activated"] = get_activated_tenants()
        app_dict["tenants_with_data_available"] = get_tenants_with_data()
        app_dict["tenants_with_public_reports"] = get_tenants_with_public_reports()

        return app_dict

    def get_serialized_reports(self):

        reports = [
            {
                k: v
                for k, v in vars(r).items()
                if k
                in [
                    "app_id",
                    "report_id",
                    "name",
                    "description",
                    "flags",
                    "url",
                    "public_url",
                    "snapshot_url",
                    "preview_image_url",
                    "preview_image_dark_url",
                    "report_components",
                    "connected_apps",
                    "filters",
                    "registrable",
                    "public_for_tenants",
                ]
            }
            for r in self.reports
        ]

        return reports

    def get_serialized_uploaders(self):

        uploaders = [
            {
                k: v
                for k, v in vars(r).items()
                if k
                in [
                    "app_id",
                    "uploader_id",
                    "name",
                    "description",
                    "accepted_file_types",
                    "flags",
                    "status",
                    "icon",
                    "upload_url",
                    "upload_validation_url",
                    "quota_validation_url",
                    "status_check_url",
                    "validation_parameters",
                    "encryption_parameters",
                    "query_params_on_upload",
                ]
            }
            for r in self.uploaders
        ]

        return uploaders

    def get_serialized_report_components(self):

        report_components = [
            {
                k: v
                for k, v in vars(r).items()
                if k
                in [
                    "app_id",
                    "component_id",
                    "url",
                    "public_url",
                    "snapshot_url",
                    "order",
                    "style_attributes",
                    "attributes",
                    "title",
                    "type",
                    "filters",
                ]
            }
            for r in self.report_components
        ]

        return report_components

    def get_register_all_payload(self):

        # Converting from objects to dictionaries
        app_dict = self.get_serialized_app_dict()
        reports = self.get_serialized_reports()
        uploaders = self.get_serialized_uploaders()
        report_components = self.get_serialized_report_components()

        payload = {
            "data": dict(
                apps=[app_dict],
                reports=reports,
                uploaders=uploaders,
                report_components=report_components,
            )
        }

        return payload

    def register_app(self):
        """
        Sending registration payloads to registry-service
        """

        payload = self.get_register_all_payload()

        register_all.send(payload)

        return payload

    def register_feature(self, feature_instance: FeatureBuilder):

        for feature in self.features:
            if feature.feature_id == feature_instance.feature_id:
                raise Exception(
                    f"Feature id '{feature_instance.feature_id}' was already declared"
                )

        self.features.append(feature_instance)

    def register_uploader(self, uploader_instance: UploaderBuilder):

        for uploader in self.uploaders:
            if uploader.uploader_id == uploader_instance.uploader_id:
                raise Exception(
                    f"Uploader id '{uploader_instance.uploader_id}' was already declared"
                )

        self.uploaders.append(uploader_instance)

    def register_report(self, report_instance: ReportBuilder):

        for report in self.reports:
            if report.report_id == report_instance.report_id:
                raise Exception(
                    f"Report id '{report_instance.report_id}' was already declared"
                )

        self.reports.append(report_instance)

    def register_report_component(self, report_component_instance: BaseReportComponent):

        for rep_component in self.report_components:
            if rep_component.component_id == report_component_instance.component_id:
                raise Exception(
                    f"Report component_id: '{report_component_instance.component_id}' was already declared"
                )

        metadata = report_component_instance.get_registration_payload()

        report_component_instance.order = (
            metadata["order"] or len(self.report_components) + 1
        )
        report_component_instance.type = metadata.pop("component_type")
        report_component_instance.style_attributes = metadata["style_attributes"]
        report_component_instance.attributes = metadata["attributes"]
        report_component_instance.filters = metadata["filters"]

        self.report_components.append(report_component_instance)

    def register_endpoint(self, endpoint_instance):
        ns = endpoint_instance.build_namespace(endpoint_builder_namespace)
        self.register_namespace(ns)

    def register_editable_table(self, editable_table_instance: EditableTable):

        for registered_table in self.editable_tables:
            registered_table: EditableTable
            if (
                registered_table.schema.__name__
                == editable_table_instance.schema.__name__
            ):
                raise Exception(
                    f"Editable table '{registered_table.schema.__name__}' already registered"
                )

        self.editable_tables.append(editable_table_instance)
        self.editable_tables_schemas.append(editable_table_instance.schema)

    def register_namespace(self, ns: Namespace, path: str = None):
        """Used for custom restx namespaces"""
        self.custom_namespaces.append((ns, path))

    def init_namespaces(self):
        for namespace in self.custom_namespaces:
            self.api.add_namespace(*namespace)

    def add_resource(self, resource: Resource, path: str):
        self.api.add_resource(resource, path)

    def add_collection(
        self, collection_name: str, db_name: str = None, timeseries_config: dict = None
    ):
        create_collection(
            collection_name=collection_name,
            db_name=db_name,
            timeseries_config=timeseries_config,
        )
