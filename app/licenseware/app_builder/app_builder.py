"""

`AppBuilder` is reponsible for creating the Api from the `X_namespace` packages and `X_route` modules. Authenticates the `App` and sends the registration information to registry-service. 

Notice that history report route/path is provided but is not implemented that's because a report must be defined with aggregated data from AnalysisStats mongo collection. 

"""

from dataclasses import dataclass
from flask_restx.resource import Resource
from app.licenseware.common.constants.envs import envs
from typing import Callable
from flask import Flask
from flask_restx import Api, Namespace
from app.licenseware.registry_service import register_all
from app.licenseware.tenants import get_activated_tenants, get_tenants_with_data
from app.licenseware.utils.logger import log
from app.licenseware.auth import Authenticator
from app.licenseware.utils.dramatiq_redis_broker import broker
from app.licenseware.utils.miscellaneous import swagger_authorization_header

from .refresh_registration_route import add_refresh_registration_route
from .editable_tables_route import add_editable_tables_route
from .tenant_registration_route import add_tenant_registration_route
from .app_activation_route import add_app_activation_route
from .app_registration_route import add_app_registration_route

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
    get_report_components_namespace
)


from .report_components_namespace import report_components_namespace
from .report_components_namespace import (
    get_report_individual_components_namespace
)


@dataclass
class base_paths:
    app_activation_path: str ='/activate_app'
    register_app_path: str = '/register_app'
    refresh_registration_path: str ='/refresh_registration'
    editable_tables_path: str ='/editable_tables'
    history_report_path: str ='/reports/history_report'
    tenant_registration_path: str ='/register_tenant'



class AppBuilder:
    
 
    def __init__(
        self, 
        name: str, 
        description: str,
        flags: list = [],
        editable_tables_schemas:list = [],
        activated_tenants_func: Callable = get_activated_tenants, 
        tenants_with_data_func: Callable = get_tenants_with_data,
        app_activation_path: str = None,
        register_app_path: str = None,
        refresh_registration_path: str = None,
        editable_tables_path: str = None,
        history_report_path: str = None,
        tenant_registration_path: str = None,
        icon: str ="default.png",
        doc_authorizations: dict = swagger_authorization_header,
        api_decorators: list = None,
        **kwargs
    ):
        
 
        self.name = name
        self.description = description
        self.flags = flags
        self.icon = icon
        self.editable_tables_schemas = editable_tables_schemas
        
        # Add to self activated tenants and tenants with data
        self.activated_tenants_func = activated_tenants_func
        self.tenants_with_data_func = tenants_with_data_func
        
        self.activated_tenants = None 
        self.tenants_with_data = None
        
        if self.activated_tenants_func:
            self.activated_tenants = self.activated_tenants_func()
        
        if self.tenants_with_data_func:
            self.tenants_with_data = self.tenants_with_data_func()
            
        self.app_activation_path = app_activation_path or base_paths.app_activation_path
        self.register_app_path = register_app_path or base_paths.register_app_path
        self.refresh_registration_path = refresh_registration_path or base_paths.refresh_registration_path
        self.editable_tables_path = editable_tables_path or base_paths.editable_tables_path
        self.history_report_path = history_report_path or base_paths.history_report_path
        self.tenant_registration_path = tenant_registration_path or base_paths.tenant_registration_path
        
        self.app_activation_url = envs.BASE_URL + self.app_activation_path
        self.refresh_registration_url = envs.BASE_URL + self.refresh_registration_path
        self.editable_tables_url = envs.BASE_URL + self.editable_tables_path
        self.history_report_url = envs.BASE_URL + self.history_report_path
        self.tenant_registration_url = envs.BASE_URL + self.tenant_registration_path

        self.authorizations = doc_authorizations
        self.decorators = api_decorators
        # parameters with default values provided can be added stright to __init__  
        # otherwise added them to kwargs until apps are actualized
        self.kwargs = kwargs    
        
        # TODO version needs to be added to all urls + '/v' + self.version
        self.prefix = '/' + envs.APP_ID 
        self.app = None
        self.api = None
        self.ns  = None
        self.reports = []
        self.report_components = []
        self.uploaders = []
        self.custom_namespaces = []
    
        self.appvars = vars(self)
    
    
    
    def init_app(self, app: Flask):
        
        # This hides flask_restx `X-fields` from swagger headers  
        app.config['RESTX_MASK_SWAGGER'] = False
        self.app = app
        
        if not self.uploaders: log.warning("No uploaders provided")
        if not self.reports  : log.warning("No reports provided")
         
        self.authenticate_app()
        self.init_dramatiq_broker()
        
        self.init_api()
        self.init_routes()
        self.init_namespaces()
        
        
    def init_dramatiq_broker(self, app:Flask = None):
        # Add middleware if needed
        broker.init_app(app or self.app)
        
    
    def authenticate_app(self):
        response, status_code = Authenticator.connect()
        if status_code != 200:
            raise Exception("App failed to authenticate!")
        return response, status_code
    
    
    def init_api(self):
        
        self.api = Api(
            app=self.app,
            title=self.name,
            description=self.description,
            prefix=self.prefix,
            default=self.name,
            default_label=self.description,
            decorators = self.decorators,
            authorizations = self.authorizations,
            security = list(self.authorizations.keys()),
            doc='/'
        )
        
        
    
    def init_routes(self):
        
        # Here we are adding the routes available for each app
        # Api must be passed from route function back to this context 
        api_funcs = [
            add_refresh_registration_route,
            add_editable_tables_route,
            add_tenant_registration_route,
            add_app_activation_route,
            add_app_registration_route
        ]
        
        for func in api_funcs:
            self.api = func(self.api, self.appvars)
        
        
        # Another way is to group routes in namespaces 
        # This way the url prefix is specified only in the namespace
        self.add_uploads_routes()
        self.add_reports_routes()
        self.add_report_components_routes()
        
    
    
    def add_uploads_routes(self):
        
        ns_funcs = [
            get_filenames_validation_namespace,
            get_filestream_validation_namespace,
            get_status_namespace,
            get_quota_namespace    
        ]
        
        for func in ns_funcs:
            self.add_namespace(
                func(ns=uploads_namespace, uploaders=self.uploaders)
            )
            
            
    def add_reports_routes(self):
        
        ns_funcs = [
            get_report_register_namespace,
            get_report_metadata_namespace,
            get_report_components_namespace
        ]
        
        for func in ns_funcs:
            self.add_namespace(
                func(ns=reports_namespace, reports=self.reports)
            )
        
        
    def add_report_components_routes(self):
        
        ns_funcs = [
            get_report_individual_components_namespace
        ]
        
        for func in ns_funcs:
            self.add_namespace(
                func(ns=report_components_namespace, report_components=self.report_components)
            )
        
                    
    def register_app(self):
        """
            Sending registration payloads to registry-service
        """
        
        # Converting from objects to dictionaries
        reports = [vars(r) for r in self.reports]
        report_components = [vars(rv) for rv in self.report_components]
        uploaders = [vars(u) for u in self.uploaders]
        
        response, status_code = register_all(
            app = self.appvars,
            reports = reports, 
            report_components = report_components, 
            uploaders = uploaders
        )
        
        if status_code != 200: raise Exception(response['message'])
        
        return response, status_code
        

    def register_uploader(self, uploader_instance):
        
        for uploader in self.uploaders:
            if uploader.uploader_id == uploader_instance.uploader_id:
                raise Exception(f"Uploader id '{uploader_instance.uploader_id}' was already declared")
        
        self.uploaders.append(uploader_instance)
        
        
    def register_report(self, report_instance):
        
        for report in self.reports:
            if report.report_id == report_instance.report_id:
                raise Exception(f"Report id '{report_instance.report_id}' was already declared")
        
        self.reports.append(report_instance)
        


    def register_report_component(self, report_component_instance):
        
        for rep_component in self.report_components:
            if rep_component.component_id == report_component_instance.component_id:
                raise Exception(f"Report component_id: '{report_component_instance.component_id}' was already declared")
                
        self.report_components.append(report_component_instance)
        
        
    def register_endpoint(self, endpoint_instance):
        ns = endpoint_instance.build_namespace(endpoint_builder_namespace)
        self.add_namespace(ns)
    
    
    def add_namespace(self, ns:Namespace, path:str = None):
        self.custom_namespaces.append((ns, path))

    def init_namespaces(self):
        for namespace in self.custom_namespaces:
            self.api.add_namespace(*namespace)
        
    def add_resource(self, resource:Resource, path:str):
        self.api.add_resource(resource, path)
    
