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
from marshmallow_jsonschema import JSONSchema
from flask_restx import Namespace, Resource
from pymongo import collection

from licenseware.common.validators import validate_uuid4
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.utils.miscellaneous import swagger_authorization_header, http_methods
from licenseware import mongodata

# from .mongo_request import MongoRequest
from flask import request
from .mongo_crud import MongoCrud






# Every api namespace generated with SchemaNamespace must have `tenant_id` and `updated_at` fields
class BaseSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    updated_at = fields.Str(required=False)






class SchemaNamespace:
    
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
        assert isinstance(self.collection, str) 
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
        
        mongo_collection_name = self.collection
        
        @ns.route("")
        class SchemaResource(Resource, MongoCrud):
            
            collection = mongo_collection_name
                    
            @ns.doc(id="Make a GET request to FETCH some data")
            @ns.param('_id', 'get data by id')
            @ns.marshal_list_with(resource_fields)
            def get(self, _id=None):
                if 'GET' in self.methods: 
                    return self.get_data(request) 
                return "METHOD NOT ALLOWED", 405

            @ns.doc(id="Make a POST request to INSERT some data")
            @ns.expect(resource_fields)
            def post(self):
                if 'POST' in self.methods:
                    return self.post_data(request) 
                return "METHOD NOT ALLOWED", 405
                
            @ns.doc(id="Make a PUT request to UPDATE some data")
            @ns.expect(resource_fields)
            def put(self):
                if 'PUT' in self.methods:
                    return self.put_data(request) 
                return "METHOD NOT ALLOWED", 405
                
            @ns.doc(id="Make a DELETE request to DELETE some data")
            @ns.expect(resource_fields)
            def delete(self, _id=None):
                if 'DELETE' in self.methods:
                    return self.delete_data(request) 
                return "METHOD NOT ALLOWED", 405

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


