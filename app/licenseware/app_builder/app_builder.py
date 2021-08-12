# import inspect
# from typing import Any, Callable, Type
# from flask import request
# from flask_restx import Namespace, , Resource

from app.licenseware.common.constants.envs import envs
from typing import Callable
from flask import Flask
from flask_restx import Api
from flask_restx.namespace import Namespace
from app.licenseware.registry_service import register_app
from app.licenseware.utils.logger import log
from app.licenseware.tenants import get_activated_tenants, get_tenants_with_data


        

authorizations = {
    'TenantId': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'TenantId'
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
        version:float = 1.0, 
        flags: list = [],
        activated_tenants_func: Callable = get_activated_tenants, 
        tenants_with_data_func: Callable = get_tenants_with_data,
        app_activation_url: str ='/app/init',
        refresh_registration_url: str ='/register_all',
        editable_tables_url: str ='/editable_tables',
        history_report_url: str ='/reports/history_report',
        tenant_registration_url: str ='/tenant_registration_url',
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
        
        # Add to self activated tenants and tenants with data
        self.activated_tenants_func = activated_tenants_func
        self.tenants_with_data_func = tenants_with_data_func
        
        self.activated_tenants = None 
        self.tenants_with_data = None
        
        if self.activated_tenants_func:
            self.activated_tenants = self.activated_tenants_func()
        
        if self.tenants_with_data_func:
            self.tenants_with_data = self.tenants_with_data_func()
            
        # Routes TODO maybe path or route instead of url is more appropiate?     
        self.app_activation_url = app_activation_url
        self.refresh_registration_url = refresh_registration_url
        self.editable_tables_url = editable_tables_url
        self.history_report_url = history_report_url
        self.tenant_registration_url = tenant_registration_url

        self.authorizations = doc_authorizations
        self.decorators = api_decorators
        # parameters with default values provided can be added stright to __init__  
        # otherwise added them to kwargs until apps are actualized
        self.kwargs = kwargs    
        
        self.prefix = '/' + self.app_id + '/v' + self.version
        self.app = None
        self.api = None
        
        self.app_vars = vars(self)
    
    
    def init_api(self, app: Flask):
        
        self.app = app
        
        api = Api(
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
        
        self.api = api
        
        
    def register_app(self):
        response, status_code = register_app(**self.app_vars)
        if status_code not in {200, 201}:
            raise Exception("App failed to register!")
        
    
    def add_namespace(self, ns:Namespace, path:str = None):
        assert path.startswith('/')
        self.api.add_namespace(ns, path=path)
    
    
    def register_uploader(self, uploader):
        uploader.register_uploader()




    #TODO's
    def register_all(self):
        register_app(**self.app_vars)
        #TODO register all uploaders, reports, etc
    
    
    def register_endpoint(self, instance):
        log.debug(instance.__name__, "registered")
            
    def register_endpoints(self, *instances):
        for instance in instances:
            self.register_endpoint(instance)
    
    
    def register_uploaders(self, *instances):
        for instance in instances:
            self.register_uploader(instance)
    
    def register_report(self, instance):
        log.debug(instance.__name__, "registered")
            
    def register_reports(self, *instances):
        for instance in instances:
            self.register_report(instance)
            
    
        
    
    
        
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
    #     self.app.add_url_rule(route, endpoint=func.__name__, view_func=func, methods=methods, **options)
    
    
    # def add_api_route(self, route:str, klass:Type, methods:list = ['GET'], **options):
    #     assert route.startswith("/")
    #     # #TODO integrate restx
    #     # self.app.add_url_rule(route, endpoint=func.__name__, view_func=func, methods=methods, **options)
        
        
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
    
    
        
    