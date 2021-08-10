import inspect
from typing import Any, Callable, Type
from flask import Flask, request
from flask_restx import Namespace, Api, Resource


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


#TODO add default decorators list 


class AppBuilder:
    
    def __init__(
        self, 
        id: str, 
        name: str, 
        description: str,
        version:float = 1.0, 
        flags: list = None,
        doc_authorizations: dict = authorizations,
        api_decorators: list = None,
        **kwargs
    ):
        
        self.id = id 
        self.name = name
        self.description = description
        self.version = str(version)
        self.flags = flags
        
        self.authorizations = doc_authorizations
        self.decorators = api_decorators
        self.kwargs = kwargs
        
        self.prefix = '/' + self.id
        self.app = None
        self.api = None
        self.namespaces = []
    
    
    def __call__(self): return self
    
    
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
        
        return api
        
        # self.add_api_namespace()
        
        # for ns in self.namespaces:
        #     api.add_namespace(ns)
        
        
    # def add_api_namespace(self, ns:Namespace = None,  name:str = None, description:str = None):   
             
    #     ns = Namespace(
    #         name = name or self.id, 
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
    #     print(args)
    #     print(kwargs)
    #     print(request)
    #     return "ok"
    
    
    # def show_param(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     print(request)
    #     return "ok"
    
    
    
    # def init_app(self, app:Flask):

        # self.app = app
        
        # self.add_app_route("/", self.index)
        # self.add_app_route("/<param>", self.show_param)
        
        # self.init_api()
    
    
        
    def register_endpoint(self, instance):
        print(instance.__name__, "registered")
            
    def register_endpoints(self, *instances):
        for instance in instances:
            self.register_endpoint(instance)
    

    def register_uploader(self, instance):
        print(instance.__name__, "registered")
    
    
    def register_uploaders(self, *instances):
        for instance in instances:
            self.register_uploader(instance)
    
    
    def register_report(self, instance):
        print(instance.__name__, "registered")
            
        
    def register_reports(self, *instances):
        for instance in instances:
            self.register_report(instance)
            
    