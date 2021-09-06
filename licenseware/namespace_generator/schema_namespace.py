import re
from inspect import signature

from marshmallow import Schema, fields
from marshmallow_jsonschema import JSONSchema
from flask_restx import Namespace, Resource

from licenseware.common.validators import validate_uuid4
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.utils.miscellaneous import swagger_authorization_header, http_methods

from .mongo_request import MongoRequest


# Every api namespace generated with SchemaNamespace must have `tenant_id` and `updated_at` fields
class BaseSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    updated_at = fields.Str(required=False)



class SchemaNamespace(MongoRequest):
    """
        This class creates the Namespace object from Schema 
        
        DeviceNamespace = SchemaNamespace(
            schema=DeviceSchema, 
            collection='IFMPData', 
            methods=['GET', 'POST']
        )

    """

    # Used by namespace decorator
    schema = None
    collection = None
    decorators = [authorization_check]
    methods = http_methods # allowed methods(the rest will get a 405)
    authorizations = swagger_authorization_header 

    def __init__(self, 
    schema: Schema = None, 
    collection: str = None, 
    methods: list = http_methods, 
    decorators: list = [authorization_check],
    authorizations: dict = swagger_authorization_header,
    namespace:Namespace = None
    ):
        self.schema = self.schema or schema
        
        # Adding `tenant_id` and `updated_at` fields to received schema
        self.schema = type(
            self.schema.__name__,
            (self.schema, BaseSchema,),
            {}
        )
        
        self.collection = self.collection or collection
        self.decorators = self.decorators or decorators
        self.methods = self.methods or methods
        self.authorizations = self.authorizations or authorizations

        self.schema_name = self.schema.__name__
        self.name = self.schema_name.replace("Schema", "")
        self.path = "/" + self.name.lower()
        self.json_schema = None
        self.ns = namespace
        self.model = None
        self.resources = None
        self.http_methods = None
        

    @classmethod
    def _initialize(cls):
        c = cls(cls.schema, cls.decorators, cls.authorizations)
        return c.initialize()

    def __call__(self):
        newcls = type(self.name, (SchemaNamespace,), {**self.__dict__})
        return newcls._initialize()
    
    def initialize(self) -> Namespace:
        """ Create restx api namespace from schema """

        self.ns = self.ns or self.create_namespace()
        self.create_indexes()
        self.make_json_schema()
        self.model = self.ns.schema_model(self.name, self.json_schema)  
        self.attach_http_methods()
        self.attach_http_docs()
        
        self.resources = self.create_resources()
        self.attach_resources()

        return self.ns

    def create_namespace(self) -> Namespace:        
        ns = Namespace(
            name = self.name, 
            description = f"API is generated from {self.schema_name}",
            decorators = self.decorators, 
            authorizations = self.authorizations,
            security = list(self.authorizations.keys())
        )
        return ns


    def create_resources(self) -> list:

        resource_list = []
        for http_verb, dict_ in self.http_methods.items():

            @self.ns.doc(**dict_['docs'])
            class BaseResource(Resource): ...
            
            resource = type(
                self.name + http_verb.capitalize(), 
                (BaseResource,), 
                {http_verb: dict_['method']}
            )

            base_route = self.path + '/' + http_verb.lower()
            routes = [base_route]

            # TODO parameters from function parameters
            # if 'params' in dict_['docs']:
            #     print("-------- params:", dict_['docs']['params'])
            #     for param in dict_['docs']['params']:
            #         routes.append(base_route + '/' + param)

            resource_list.append((resource, *routes))

        return resource_list


    def attach_resources(self):
        for resource in self.resources:
            self.ns.add_resource(*resource)


    def attach_http_methods(self):
     
        if self.http_methods: return

        methods = [m.lower() for m in self.methods]
        
        self.http_methods = {}
        for method in methods:
            if method == 'get':
                self.http_methods[method] = {'method': self.get, 'docs': None}
            if method == 'post':
                self.http_methods[method] = {'method': self.post, 'docs': None}
            if method == 'put':
                self.http_methods[method] = {'method': self.put, 'docs': None}
            if method == 'delete':
                self.http_methods[method] = {'method': self.delete, 'docs': None}
        

    def attach_http_docs(self):

        for k in self.http_methods.keys():
            self.http_methods[k]['docs'] = {
                'id': f'{k.upper()} request for {self.name}',
                'description': f'Make a {k.upper()} request on {self.name} data.',
                'responses':{
                    200: 'SUCCESS',
                    500: 'INTERNAL SERVER ERROR',
                    401: 'UNAUTHORIZED',
                    405: 'METHOD NOT ALLOWED',
                },
                'model':self.model,
                'security': list(self.authorizations.keys())
            }

            if k in ['post', 'put', 'delete']:
                self.http_methods[k]['docs'].update({'body':self.model})

            sig = signature(self.http_methods[k]['method'])
            raw_params = list(dict(sig.parameters).keys())
            
            if raw_params:
                self.http_methods[k]['docs'].update({"params": {}})
                for param_name in raw_params:
                    param_type = re.search(r"<class '(.*?)'>", str(sig.parameters[param_name].annotation)).group(1)
                    param_type = 'str' if param_type == 'inspect._empty' else param_type
                    self.http_methods[k]['docs']["params"].update(
                        { param_name:  f"Query parameter ({param_type})"}
                    )

                
    def make_json_schema(self) -> dict:
        self.json_schema = JSONSchema().dump(self.schema())["definitions"][self.schema_name]


