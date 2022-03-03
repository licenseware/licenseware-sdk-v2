"""

`AppBuilder` is reponsible for creating the Api from the `X_namespace` packages and `X_route` modules. Authenticates the `App` and sends the registration information to registry-service. 

Notice that history report route/path is provided but is not implemented that's because a report must be defined with aggregated data from AnalysisStats mongo collection. 

"""

from typing import List, Callable
from dataclasses import dataclass

from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Namespace, Resource
from marshmallow.schema import Schema

from licenseware.uploader_builder.uploader_builder import UploaderBuilder
from licenseware.report_builder.report_builder import ReportBuilder
from licenseware.report_components.base_report_component import BaseReportComponent
from licenseware.feature_builder import FeatureBuilder
from licenseware.common.constants.envs import envs
from licenseware.registry_service import register_all
from licenseware.tenants import get_activated_tenants, get_tenants_with_data
from licenseware.utils.logger import log
from licenseware.auth import Authenticator
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.miscellaneous import swagger_authorization_header
from licenseware.editable_table import EditableTable
from licenseware.schema_namespace import SchemaNamespace

from .refresh_registration_route import add_refresh_registration_route
from .editable_tables_route import add_editable_tables_route
from .tenant_registration_route import add_tenant_registration_route
from .app_activation_route import add_app_activation_route
from .app_registration_route import add_app_registration_route
from .terms_and_conditions_route import add_terms_and_conditions_route
from .features_route import add_features_route

from .endpoint_builder_namespace import endpoint_builder_namespace

from .uploads_namespace import uploads_namespace
from .uploads_namespace import (
    get_filenames_validation_namespace,
    get_filestream_validation_namespace,
    get_status_namespace,
    get_quota_namespace
)

from .reports_namespace import reports_namespace
from .reports_namespace import (
    get_report_register_namespace,
    get_report_metadata_namespace,
    get_report_components_namespace,
    get_report_image_preview_namespace,
    get_report_image_preview_dark_namespace
)

from .report_components_namespace import report_components_namespace
from .report_components_namespace import (
    get_report_individual_components_namespace
)

from .features_namespace import features_namespace
from .features_namespace import (
    get_features_namespace
)

from .download_as_route import add_download_as_route


@dataclass
class base_paths:
    app_activation_path: str = '/activate_app'
    register_app_path: str = '/register_app'
    refresh_registration_path: str = '/refresh_registration'
    editable_tables_path: str = '/editable_tables'
    history_report_path: str = '/reports/history_report'
    tenant_registration_path: str = '/register_tenant'
    terms_and_conditions_path: str = '/terms_and_conditions'
    features_path: str = '/features'


class AppBuilder:

    def __init__(
            self,
            name: str,
            description: str,
            flags: list = [],
            features: List[FeatureBuilder] = [],
            editable_tables: List[EditableTable] = [],
            app_meta: dict = None,
            activated_tenants_func: Callable = get_activated_tenants,
            tenants_with_data_func: Callable = get_tenants_with_data,
            app_activation_path: str = None,
            register_app_path: str = None,
            refresh_registration_path: str = None,
            editable_tables_path: str = None,
            history_report_path: str = None,
            tenant_registration_path: str = None,
            terms_and_conditions_path: str = None,
            features_path: str = None,
            icon: str = "default.png",
            doc_authorizations: dict = swagger_authorization_header,
            api_decorators: list = None,
            editable_tables_schemas: List[Schema] = [],
            **options
    ):

        self.name = name
        self.app_id = envs.APP_ID

        if envs.DEPLOYMENT_SUFFIX is not None:
            self.name = self.name + envs.DEPLOYMENT_SUFFIX
            self.app_id = self.app_id + envs.DEPLOYMENT_SUFFIX

        self.description = description
        self.features = features
        self.flags = flags
        self.icon = icon
        self.editable_tables = editable_tables
        self.editable_tables_schemas = editable_tables_schemas
        self.app_meta = app_meta
        # Add to self activated tenants and tenants with data
        self.activated_tenants_func = activated_tenants_func
        self.tenants_with_data_func = tenants_with_data_func
        self.activated_tenants = None
        self.tenants_with_data = None

        self.app_activation_path = app_activation_path or base_paths.app_activation_path
        self.register_app_path = register_app_path or base_paths.register_app_path
        self.refresh_registration_path = refresh_registration_path or base_paths.refresh_registration_path
        self.editable_tables_path = editable_tables_path or base_paths.editable_tables_path
        self.history_report_path = history_report_path or base_paths.history_report_path
        self.tenant_registration_path = tenant_registration_path or base_paths.tenant_registration_path
        self.terms_and_conditions_path = terms_and_conditions_path or base_paths.terms_and_conditions_path
        self.features_path = features_path or base_paths.features_path

        self.app_activation_url = envs.BASE_URL + self.app_activation_path
        self.refresh_registration_url = envs.BASE_URL + self.refresh_registration_path
        self.editable_tables_url = envs.BASE_URL + self.editable_tables_path
        self.history_report_url = envs.BASE_URL + self.history_report_path
        self.tenant_registration_url = envs.BASE_URL + self.tenant_registration_path
        self.terms_and_conditions_url = envs.BASE_URL + self.terms_and_conditions_path
        self.features_url = envs.BASE_URL + self.features_path

        self.authorizations = doc_authorizations
        self.decorators = api_decorators
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

    def init_app(
            self,
            app: Flask,
            register: bool = False
    ):

        # This hides flask_restx `X-fields` from swagger headers  
        app.config['RESTX_MASK_SWAGGER'] = False

        @app.after_request
        def after_request(response):
            response.headers.set('Access-Control-Allow-Origin', '*')
            response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization,TenantId,Tenantid')
            response.headers.set('Access-Control-Allow-Methods',
                                 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.set('Access-Control-Allow-Credentials', 'true')

            return response

        # CORS(app)

        self.app = app

        if not self.uploaders: log.warning("No uploaders provided")
        if not self.reports: log.warning("No reports provided")

        self.authenticate_app()
        self.init_api()
        self.init_routes()
        self.init_namespaces()
        self.init_broker()
        if register: self.register_app()

        return self.app

    def init_broker(self, app: Flask = None):
        self.broker = broker.init_app(app or self.app)
        return self.broker

    def authenticate_app(self):
        response, status_code = Authenticator.connect(max_retries='infinite', wait_seconds=2)
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
            doc=self.prefix + '/docs'
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
            add_features_route
        ]

        for func in api_funcs:
            self.api = func(self.api, self.appvars)

        # Another way is to group routes in namespaces 
        # This way the url prefix is specified only in the namespace
        self.add_uploads_routes()
        self.add_reports_routes()
        self.add_report_components_routes()
        self.add_editables_routes()
        self.add_features_routes()

    def add_uploads_routes(self):

        ns_funcs = [
            get_filenames_validation_namespace,
            get_filestream_validation_namespace,
            get_status_namespace,
            get_quota_namespace
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
            get_report_image_preview_dark_namespace
        ]

        for func in ns_funcs:
            self.register_namespace(
                func(ns=reports_namespace, reports=self.reports)
            )

    def add_report_components_routes(self):

        ns_funcs = [
            get_report_individual_components_namespace
        ]

        for func in ns_funcs:
            self.register_namespace(
                func(ns=report_components_namespace, report_components=self.report_components)
            )

    def add_editables_routes(self):

        for editable in self.editable_tables:
            if editable.namespace:
                self.register_namespace(editable.namespace)
            else:
                ns = SchemaNamespace(schema=editable.schema).initialize()
                self.register_namespace(ns)

    def add_features_routes(self):

        ns_funcs = [
            get_features_namespace
        ]

        for func in ns_funcs:
            self.register_namespace(
                func(ns=features_namespace, features=self.features)
            )

    def register_app(self):
        """
            Sending registration payloads to registry-service
        """

        # Converting from objects to dictionaries

        app_dict = \
            {k: v
             for k, v in self.appvars.items() if k in [
                 'app_id',
                 'name',
                 'description',
                 'flags',
                 'icon',
                 'refresh_registration_url',
                 'app_activation_url',
                 'editable_tables_url',
                 'history_report_url',
                 'tenant_registration_url',
                 'terms_and_conditions_url',
                 'features_url',
                 'app_meta'
             ]
             }

        app_dict['features'] = [f.get_details() for f in self.features]
        app_dict['tenants_with_app_activated'] = self.activated_tenants_func()
        app_dict['tenants_with_data_available'] = self.tenants_with_data_func()

        reports = \
            [
                {k: v
                 for k, v in vars(r).items()
                 if k in [
                     'app_id',
                     'report_id',
                     'name',
                     'description',
                     'flags',
                     'url',
                     'preview_image_url',
                     'preview_image_dark_url',
                     'report_components',
                     'connected_apps',
                     'filters',
                     'registrable'
                 ]
                 }
                for r in self.reports
            ]

        uploaders = \
            [
                {k: v
                 for k, v in vars(r).items()
                 if k in [
                     'app_id',
                     'uploader_id',
                     'name',
                     'description',
                     'accepted_file_types',
                     'flags',
                     'status',
                     'icon',
                     'upload_url',
                     'upload_validation_url',
                     'quota_validation_url',
                     'status_check_url',
                     'validation_parameters'
                 ]
                 }
                for r in self.uploaders
            ]

        report_components = \
            [
                {k: v
                 for k, v in vars(r).items()
                 if k in [
                     'app_id',
                     'component_id',
                     'url',
                     'order',
                     'style_attributes',
                     'attributes',
                     'title',
                     'component_type',
                     'filters'
                 ]
                 }
                for r in self.report_components
            ]

        payload = {
            'data': dict(
                apps=[app_dict],
                reports=reports,
                uploaders=uploaders,
                report_components=report_components
            )
        }

        register_all.send(payload)

        return payload

    def register_feature(self, feature_instance: FeatureBuilder):

        for feature in self.features:
            if feature.feature_id == feature_instance.feature_id:
                raise Exception(f"Feature id '{feature_instance.feature_id}' was already declared")

        self.features.append(feature_instance)

    def register_uploader(self, uploader_instance: UploaderBuilder):

        for uploader in self.uploaders:
            if uploader.uploader_id == uploader_instance.uploader_id:
                raise Exception(f"Uploader id '{uploader_instance.uploader_id}' was already declared")

        self.uploaders.append(uploader_instance)

    def register_report(self, report_instance: ReportBuilder):

        for report in self.reports:
            if report.report_id == report_instance.report_id:
                raise Exception(f"Report id '{report_instance.report_id}' was already declared")

        self.reports.append(report_instance)

    def register_report_component(self, report_component_instance: BaseReportComponent):

        for rep_component in self.report_components:
            if rep_component.component_id == report_component_instance.component_id:
                raise Exception(f"Report component_id: '{report_component_instance.component_id}' was already declared")

        metadata = report_component_instance.get_registration_payload()

        report_component_instance.order = metadata['order'] or len(self.report_components) + 1
        report_component_instance.type = metadata.pop('component_type')
        report_component_instance.style_attributes = metadata['style_attributes']
        report_component_instance.attributes = metadata['attributes']
        report_component_instance.filters = metadata['filters']

        self.report_components.append(report_component_instance)

    def register_endpoint(self, endpoint_instance):
        ns = endpoint_instance.build_namespace(endpoint_builder_namespace)
        self.register_namespace(ns)

    def register_editable_table(self, editable_table_instance: EditableTable):

        for registered_table in self.editable_tables:
            registered_table: EditableTable
            if registered_table.schema.__name__ == editable_table_instance.schema.__name__:
                raise Exception(f"Editable table '{registered_table.schema.__name__}' already registered")

        self.editable_tables.append(editable_table_instance)
        self.editable_tables_schemas.append(editable_table_instance.schema)

    def register_namespace(self, ns: Namespace, path: str = None):
        """ Used for custom restx namespaces """
        self.custom_namespaces.append((ns, path))

    def init_namespaces(self):
        for namespace in self.custom_namespaces:
            self.api.add_namespace(*namespace)

    def add_resource(self, resource: Resource, path: str):
        self.api.add_resource(resource, path)
