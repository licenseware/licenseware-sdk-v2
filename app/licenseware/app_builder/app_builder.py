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
from .uploads_filenames_validation_routes import add_uploads_filenames_validation_routes
from .uploads_filestream_validation_routes import add_uploads_filestream_validation_routes
from .uploads_status_routes import add_uploads_status_routes
from .uploads_quota_routes import add_uploads_quota_routes
from .tenant_registration_route import add_tenant_registration_route


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
        app_activation_path: str ='/app/init',
        refresh_registration_path: str ='/register_all',
        editable_tables_path: str ='/editable_tables',
        history_report_path: str ='/reports/history_report',
        tenant_registration_path: str ='/tenant_registration',
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
        
        self.app_vars = vars(self)
    
    
    def init_app(self, app: Flask, register:bool =True):
        
        self.app = app
        
        if not self.uploaders: log.warning("No uploaders provided")
        if not self.reports  : log.warning("No reports provided")
         
        self.authenticate_app()
        self.init_api()
        self.add_default_routes()
        if register: self.register_app()
        self.init_dramatiq_broker()
        
        
    def init_dramatiq_broker(self):
        # Add middleware if needed
        broker.init_app(self.app)
        
        
        
   
    def authenticate_app(self):
        response, status_code = Authenticator.connect()
        if status_code != 200:
            raise Exception("App failed to authenticate!")
    
    
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
        
        self.api = add_uploads_filenames_validation_routes(self.api, self.uploaders)
        self.api = add_uploads_filestream_validation_routes(self.api, self.uploaders)
        self.api = add_uploads_status_routes(self.api, self.uploaders)
        self.api = add_uploads_quota_routes(self.api, self.uploaders)
        
                    
                    
    def register_app(self):
        response, status_code = register_app(**self.app_vars)
        if status_code not in {200, 201}:
            raise Exception("App failed to register!")
            
        
    def register_uploader(self, uploader_instance):
        
        for uploader in self.uploaders:
            if uploader.uploader_id == uploader_instance.uploader_id:
                raise Exception(f"Uploader id '{uploader_instance.uploader_id}' was already declared")
        
        self.uploaders.append(uploader_instance)
        
        response, status_code = uploader_instance.register_uploader()
        if status_code not in {200, 201}:
            raise Exception("Uploader failed to register!")



    def add_namespace(self, ns:Namespace, path:str = None):
        self.api.add_namespace(ns, path=path)
        
    def add_resource(self, resource:Resource, path:str):
        self.api.add_resource(resource, path)
    


    # #TODO's
    # def register_all(self):
    #     register_app(**self.app_vars)
    #     #TODO register all uploaders, reports, etc
    
    
    # def register_endpoint(self, instance):
    #     log.debug(instance.__name__, "registered")
            
    # def register_endpoints(self, *instances):
    #     for instance in instances:
    #         self.register_endpoint(instance)
    
    
    # def register_uploaders(self, *instances):
    #     for instance in instances:
    #         self.register_uploader(instance)
    
    # def register_report(self, instance):
    #     log.debug(instance.__name__, "registered")
            
    # def register_reports(self, *instances):
    #     for instance in instances:
    #         self.register_report(instance)
            
    
        
        # self.add_api_namespace()
        
        # for ns in self.namespaces:
        #     api.add_namespace(ns)
        
        
    # def add_api_namespace(self, ns:Namespace = None,  name:str = None, description:str = None):   
             
    #     ns = Namespace(
    #         name = name or self.app_id, 
    #         description = description or self.description
    #     )
        
    #     @ns.route('/hello')
    #     class HelloWorld(Resource):
    #         def get(self):
    #             return {'hello': 'world'}

        
    #     self.namespaces.append(ns)
            
        
            
            
    # def add_route(self, handler:Any, route:str = None, methods:list = ['GET'], **options):
        
    #     methods += self.http_methods_from_handler(handler)
        
    #     if inspect.isclass(handler):
    #         self.add_api_route(route, handler, methods, **options)
    
    #     if inspect.isfunction(handler):
    #         self.add_app_route(route, handler, methods, **options)
    
    #     raise ValueError("Parameter handler can be only a function or a class")
        
        
    # def http_methods_from_handler(self, handler: Any):
        
    #     methods = []
        
    #     handler_name = handler.__name__.upper()
        
    #     # GET is available by default
        
    #     if handler_name.startswith("POST"):
    #         methods.append("POST")
        
    #     if handler_name.startswith("PUT"):
    #         methods.append("PUT")
        
    #     if handler_name.startswith("DELETE"):
    #         methods.append("DELETE")
            
    #     return methods
        
    
    # def add_app_route(self, route:str, func:Callable, methods:list = ['GET'], **options):
    #     assert route.startswith("/")
    #     self.app.add_path_rule(route, endpoint=func.__name__, view_func=func, methods=methods, **options)
    
    
    # def add_api_route(self, route:str, klass:Type, methods:list = ['GET'], **options):
    #     assert route.startswith("/")
    #     # #TODO integrate restx
    #     # self.app.add_path_rule(route, endpoint=func.__name__, view_func=func, methods=methods, **options)
        
        
    # def index(self, *args, **kwargs):
    #     log.debug(args)
    #     log.debug(kwargs)
    #     log.debug(request)
    #     return "ok"
    
    
    # def show_param(self, *args, **kwargs):
    #     log.debug(args)
    #     log.debug(kwargs)
    #     log.debug(request)
    #     return "ok"
    
    
    
    # def init_app(self, app:Flask):

        # self.app = app
        
        # self.add_app_route("/", self.index)
        # self.add_app_route("/<param>", self.show_param)
        
        # self.init_api()
    
    
        
    