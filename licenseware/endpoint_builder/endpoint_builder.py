from typing import Any
from flask_restx import Namespace, Resource
from licenseware.utils.miscellaneous import http_methods
from licenseware.utils.logger import log
from licenseware.schema_namespace import SchemaNamespace
import inspect




class EndpointBuilder:
    
    """
    Usage: 
    
    from licenseware.endpoint_builder import EndpointBuilder
    
    index_endpoint = EndpointBuilder(
        handler = get_some_data,
        **options
    )
    
    Params:
    
    - handler: function or schema
    - options: provided as a quick had for extending functionality, once one options param is stable it can be added to params
    
    """
    
    def __init__(
        self, 
        handler: Any, 
        http_method:str = None,
        http_path:str = None,
        docid:str = None,
        **options
    ):
        
        self.handler = handler
        self.options = options
    
        self.http_method = http_method
        self.http_path = http_path
        self.docid = docid or handler.__doc__ or handler.__name__.replace('_', ' ')
        
        self.initialize()
        
    
    
    def build_namespace(self, ns: Namespace):
        
        if inspect.isfunction(self.handler):
            ns = self.add_method_to_namespace(ns)
            return ns
        
        if '_Schema__apply_nested_option' in dir(self.handler):
            
            schema_ns = SchemaNamespace(
                schema = self.handler,
                collection = self.handler.Meta.collection_name,
                namespace = ns
            ).initialize()
            
            return schema_ns
        
        raise Exception("Parameter `handler` can be only a function or a marshmellow schema")
        
    
    def initialize(self):
        self.set_http_method()
        self.set_http_path()
    
    
    def add_method_to_namespace(self, ns):
        
        @ns.doc(id=self.docid)
        class BaseResource(Resource): ...
            
        resource = type(
            self.handler.__name__ + self.http_method.capitalize(), 
            (BaseResource,), 
            {self.http_method.lower(): lambda request: self.handler(request)}
        )
        
        ns.add_resource(resource, self.http_path) 
        
        return ns
        
        
    def set_http_path(self):
        if self.http_path: return 
        self.http_path = '/' + self.handler.__name__.lower()
    
    
    def set_http_method(self):
        if self.http_method: return
        handler_name = self.handler.__name__.upper()
        for httpmethod in http_methods:
            if handler_name.startswith(httpmethod):
                self.http_method = httpmethod
                break
        
            