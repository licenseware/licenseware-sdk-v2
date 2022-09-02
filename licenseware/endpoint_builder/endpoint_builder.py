"""

Bellow is an example on how you can use the endpoint builder

```py

from flask import request
from licenseware import mongodata
from licenseware.endpoint_builder import EndpointBuilder


# Specify the http method 
def get_detected_uploaders(): # a function that takes no parameters
    
    event_id  = request.args.get("event_id")
    tenant_id = request.headers.get("Tenantid")
    
    results = mongodata.fetch(
        collection="DetectedUploaders",
        match={
            'tenant_id': tenant_id,
            'event_id': event_id
        }
    )
    
    return results


# Declare the swagger docs in a dict (if needed)
swagger_docs = {
    'get': {
        'description': 'Get detected uploaders for the app provided', 
        'params': {
            'event_id': { 'description': 'The uuid4 received on when filenames were sent to uploader detector' }
        },
        'responses': { 
            200: 'Success', 
            403: 'Missing `Tenantid` or `Authorization` information', 
            500: 'Something went wrong while handling the request'
        }
    }
}

# Instantiate the EndpointBuilder class
get_detected_uploaders_endpoint = \
EndpointBuilder(
    handler = get_detected_uploaders,
    swagger = swagger_docs
)

# Later register it to the main App
App.register_enpoint(get_detected_uploaders_endpoint)

```



"""

import inspect
from typing import Any

from flask_restx import Namespace, Resource

from licenseware.schema_namespace import SchemaNamespace
from licenseware.utils.miscellaneous import http_methods


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
        swagger: dict = None,
        http_method: str = None,
        http_path: str = None,
        **options
    ):

        self.handler = handler
        self.options = options
        self.apidoc = swagger

        self.http_method = http_method
        self.http_path = http_path
        self.doc_id = handler.__name__.replace("_", " ")
        self.doc_description = handler.__doc__

        self.initialize()

    def build_namespace(self, ns: Namespace):

        if inspect.isfunction(self.handler):
            ns = self.add_method_to_namespace(ns)
            return ns

        if "_Schema__apply_nested_option" in dir(self.handler):

            schema_ns = SchemaNamespace(
                schema=self.handler,
                collection=self.handler.Meta.collection_name,
                namespace=ns,
            ).initialize()

            return schema_ns

        raise Exception(
            "Parameter `handler` can be only a function or a marshmellow schema"
        )

    def initialize(self):
        self.set_http_method()
        self.set_http_path()

    def add_method_to_namespace(self, ns):

        if self.apidoc:

            class BaseResource(Resource):
                ...

            BaseResource.__apidoc__ = self.apidoc
        else:

            @ns.doc(id=self.doc_id, description=self.doc_description)
            class BaseResource(Resource):
                ...

        CResource = type(
            self.handler.__name__ + self.http_method.capitalize(),
            (BaseResource,),
            {self.http_method.lower(): lambda _: self.handler()},
        )

        ns.add_resource(CResource, self.http_path)

        return ns

    def set_http_path(self):
        if self.http_path:
            return
        self.http_path = "/" + "_".join(self.handler.__name__.lower().split("_")[1:])

    def set_http_method(self):
        if self.http_method:
            return
        handler_name = self.handler.__name__.upper()
        for httpmethod in http_methods:
            if handler_name.startswith(httpmethod):
                self.http_method = httpmethod
                break
