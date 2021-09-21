"""
# TODO docs

This class creates the Namespace object from Schema 

DeviceNamespace = SchemaNamespace(
    schema=DeviceSchema, 
    collection='IFMPData', 
    methods=['GET', 'POST']
)



"""


import re
from inspect import signature

from marshmallow import Schema, fields
import marshmallow
from marshmallow_jsonschema import JSONSchema
from flask_restx import Namespace, Resource

from licenseware.common.validators import validate_uuid4
from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators.failsafe_decorator import failsafe
from licenseware.utils.miscellaneous import swagger_authorization_header, http_methods
from licenseware.utils.logger import log
from licenseware import mongodata


from flask import request
from .mongo_crud import MongoCrud






# Every api namespace generated with SchemaNamespace must have `tenant_id` and `updated_at` fields
class BaseSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    updated_at = fields.Str(required=False)



class SchemaNamespace:
    
    def __init__(self, 
    schema: Schema = None, 
    collection: str = None, 
    methods: list = http_methods, 
    decorators: list = [authorization_check],
    authorizations: dict = swagger_authorization_header,
    mongo_crud_class: type = MongoCrud,
    namespace: Namespace = None
    ):
        self.schema = schema
        
        # Adding `tenant_id` and `updated_at` fields to received schema
        self.schema = type(
            self.schema.__name__,
            (self.schema, BaseSchema,),
            {}
        )
        
    
        try: self.collection = self.schema.Meta.collection
        except: self.collection = collection or envs.MONGO_COLLECTION_DATA_NAME
        
        try: self.methods = self.schema.Meta.methods
        except: self.methods = methods
        
        self.decorators = decorators
        self.authorizations = authorizations
        self.mongo_crud_class = mongo_crud_class
        self.namespace = namespace

        self.schema_name = self.schema.__name__
        self.name = self.schema_name.replace("Schema", "")
        self.path = "/" + self.name.lower()
        self.json_schema = None

    
    def initialize(self) -> Namespace:
        """ Create restx api namespace from schema """

        self.create_indexes()
        self.make_json_schema()
        ns = self.create_resources()
        
        return ns


    def create_namespace(self) -> Namespace:        
        ns = Namespace(
            name = self.name, 
            path = self.path,
            description = f"API is generated from {self.schema_name}",
            decorators = self.decorators, 
            authorizations = self.authorizations,
            security = list(self.authorizations.keys())
        )
        return ns


    def create_resources(self) -> list:
        
        ns = self.create_namespace()
        resource_fields = ns.schema_model(self.name, self.json_schema)  
        
        self.mongo_crud_class.schema = self.schema
        self.mongo_crud_class.collection = self.collection
        allowed_methods = self.methods
        
        CrudClass = self.mongo_crud_class
        
        class SchemaResource(Resource, CrudClass):
        
            @failsafe(fail_code=500)
            @ns.doc(id="Make a GET request to FETCH some data")
            @ns.param('_id', 'get data by id')
            @ns.marshal_list_with(resource_fields)
            def get(self):
                if 'GET' in allowed_methods: 
                    return self.get_data(request) 
                return "METHOD NOT ALLOWED", 405

            @failsafe(fail_code=500)
            @ns.doc(id="Make a POST request to INSERT some data")
            @ns.expect(resource_fields)
            def post(self):
                if 'POST' in allowed_methods:
                    return self.post_data(request) 
                return "METHOD NOT ALLOWED", 405
                
            @failsafe(fail_code=500)
            @ns.doc(id="Make a PUT request to UPDATE some data")
            @ns.expect(resource_fields)
            def put(self):
                if 'PUT' in allowed_methods:
                    return self.put_data(request) 
                return "METHOD NOT ALLOWED", 405
            
            @failsafe(fail_code=500)
            @ns.doc(id="Make a DELETE request to DELETE some data")
            @ns.expect(resource_fields)
            def delete(self, _id=None):
                if 'DELETE' in allowed_methods:
                    return self.delete_data(request) 
                return "METHOD NOT ALLOWED", 405
            
        
        ns.add_resource(SchemaResource, "")

        return ns
        
        
    def create_indexes(self):
        
        coll = mongodata.get_collection(self.collection)
        
        try:
            for i in self.schema.Meta.simple_indexes:
                coll.create_index(i)
        except AttributeError:
            # log.info("No simple indexes declared")
            pass
        
        try:
            for ci in self.schema.Meta.compound_indexes:
                col_list = [(ci_m, 1) for ci_m in ci]
                coll.create_index(col_list, unique=True)
        except AttributeError:
            # log.info("No compound indexes declared")
            pass


    def make_json_schema(self) -> dict:
        self.json_schema = JSONSchema().dump(self.schema())["definitions"][self.schema_name]


