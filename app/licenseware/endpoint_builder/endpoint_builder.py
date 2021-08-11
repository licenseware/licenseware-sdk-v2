from typing import Callable
from marshmallow import Schema



class EndpointBuilder:
    
    """
    Usage: 
    
    from app.licenseware.endpoint_builder import EndpointBuilder
    
    index_endpoint = EndpointBuilder(
        route = "/",
        http_method = "GET",
        handler_method = get_some_data,
        schema = DataSchema
        **kwargs
    )
    
    Params:
    
    - route: optional, will use `handler_method` name if not present, 
            route will be appended to app_id route ex: '/ifmp/{here}'
             
    - http_method: optional, will use `handler_method` prefix name if not present 
                   (ex: get_some_data -> 'GET', post_some_data -> 'POST'),

    - handler_method: required if schema not provided, will receive as parameter flask `request` object by default 
    
    - schema: required if handler_method not provided, will generate a CRUD api based on schema
    
    - kwargs: provided as a quick had for extending functionality, once one kwargs param is stable it can be added to params
    
    """
    
    def __init__(
        self, 
        handler_method: Callable = None, 
        schema: str = None,
        route: str = None,
        http_method: str = None, 
        **kwargs
    ):
        
        assert handler_method or schema
        
        self.route = route
        self.http_method = http_method
        self.handler_method = handler_method
        self.schema = schema
        self.kwargs = kwargs