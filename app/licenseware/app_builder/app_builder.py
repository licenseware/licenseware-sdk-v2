from flask_restx.resource import Resource
from app.licenseware.common.constants.envs import envs
from typing import Callable
from flask import Flask
from flask_restx import Api, Namespace
from app.licenseware.registry_service import register_app
from app.licenseware.tenants import get_activated_tenants, get_tenants_with_data
from app.licenseware.utils.logger import log
from app.licenseware.auth import Authenticator
from app.licenseware.utils.dramatiq_redis_broker import broker

from .register_all_route import add_register_all_route
from .editable_tables_route import add_editable_tables_route
from .app_route import add_app_route
from .app_activation_route import add_app_activation_route
from .tenant_registration_route import add_tenant_registration_route


from .uploads_namespace import uploads_namespace
from .uploads_namespace import (
    get_filenames_validation_namespace,
    get_filestream_validation_namespace,
    get_status_namespace,
    get_quota_namespace
)




# TODO TenantId is not posible 
# because either flask or swagger capitalizes values from headers 

authorizations = {
    'Tenantid': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Tenantid'   #TenantId
    },
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


class AppBuilder:
    
    def __init__(
        self, 
        name: str, 
        description: str,
        flags: list = [],
        version:int = 1, 
        editable_tables_schemas:list = [],
        activated_tenants_func: Callable = get_activated_tenants, 
        tenants_with_data_func: Callable = get_tenants_with_data,
        app_activation_path: str ='/activate_app',
        register_app_path: str = '/register_app',
        refresh_registration_path: str ='/refresh_registration',
        editable_tables_path: str ='/editable_tables',
        history_report_path: str ='/reports/history_report',
        tenant_registration_path: str ='/register_tenant',
        icon: str ="default.png",
        doc_authorizations: dict = authorizations,
        api_decorators: list = None,
        **kwargs
    ):
        
        self.app_id = envs.APP_ID 
        self.name = name
        self.description = description
        self.version = str(version)
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
            
        self.app_activation_path = app_activation_path
        self.register_app_path = register_app_path
        self.refresh_registration_path = refresh_registration_path
        self.editable_tables_path = editable_tables_path
        self.history_report_path = history_report_path
        self.tenant_registration_path = tenant_registration_path
        
        self.app_activation_url = envs.BASE_URL + app_activation_path
        self.refresh_registration_url = envs.BASE_URL + refresh_registration_path
        self.editable_tables_url = envs.BASE_URL + editable_tables_path
        self.history_report_url = envs.BASE_URL + history_report_path
        self.tenant_registration_url = envs.BASE_URL + tenant_registration_path

        self.authorizations = doc_authorizations
        self.decorators = api_decorators
        # parameters with default values provided can be added stright to __init__  
        # otherwise added them to kwargs until apps are actualized
        self.kwargs = kwargs    
        
        self.prefix = '/' + self.app_id + '/v' + self.version
        self.app = None
        self.api = None
        self.ns  = None
        self.reports = []
        self.uploaders = []
        self.custom_namespaces = []
    
    
    
    def init_app(self, app: Flask, register:bool =True):
        
        if not self.uploaders: log.warning("No uploaders provided")
        if not self.reports  : log.warning("No reports provided")
         
        self.app = app
        self.authenticate_app()
        self.init_dramatiq_broker()
        if register: self.register_app()
        
        self.init_api()
        self.add_default_routes()
        self.init_namespaces()
        
        
    def init_dramatiq_broker(self):
        # Add middleware if needed
        broker.init_app(self.app)
        
    
    def authenticate_app(self):
        response, status_code = Authenticator.connect()
        if status_code != 200:
            raise Exception("App failed to authenticate!")
        return response, status_code
    
    
    def init_api(self):
        
        self.api = Api(
            app=self.app,
            title=self.name,
            version=self.version,
            description=self.description,
            prefix=self.prefix,
            default=self.name,
            default_label=self.description,
            decorators = self.decorators,
            authorizations = self.authorizations,
            security = list(self.authorizations.keys()),
            doc='/'
        )
        
        
    
    def add_default_routes(self):
        
        # Here we are adding the routes available for each app
        # Api must be passed from route function back to this context
    
        self.api = add_app_route(self.api, self.app_vars)
        self.api = add_app_activation_route(self.api, self.app_vars, self.uploaders)
        self.api = add_register_all_route(self.api, self.reports, self.uploaders)
        self.api = add_editable_tables_route(self.api, self.editable_tables_schemas)
        self.api = add_tenant_registration_route(self.api, self.app_vars)
        
        self.add_uploads_routes()
        
        
        # TODO Reports should be on the Reports Namespace with /reports prefix
        
    
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
        
                    
    def register_app(self):
        
        response, status_code = register_app(**vars(self))
        
        if status_code not in {200, 201}:
            raise Exception("App failed to register!")
        
        return response, status_code
            
        
    def register_uploader(self, uploader_instance):
        
        for uploader in self.uploaders:
            if uploader.uploader_id == uploader_instance.uploader_id:
                raise Exception(f"Uploader id '{uploader_instance.uploader_id}' was already declared")
        
        self.uploaders.append(uploader_instance)
        
        response, status_code = uploader_instance.register_uploader()
        
        if status_code not in {200, 201}:
            raise Exception("Uploader failed to register!")
        
        return response, status_code



    def add_namespace(self, ns:Namespace, path:str = None):
        self.custom_namespaces.append((ns, path))

    def init_namespaces(self):
        for namespace in self.custom_namespaces:
            self.api.add_namespace(*namespace)
        
        
    def add_resource(self, resource:Resource, path:str):
        self.api.add_resource(resource, path)
    
