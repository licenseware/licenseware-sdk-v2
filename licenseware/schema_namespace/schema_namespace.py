"""

Class `SchemaNamespace` can be used to generate a restx namespace from a marshmallow schema.

A minimal example would be this:

```py

from marshmallow import Schema, fields
from licenseware.schema_namespace import SchemaNamespace

class UserSchema(Schema):
    ''' Here is some namespace doc for user namespace '''
    name = fields.Str(required=True)
    occupation = fields.Str(required=True)
    
    
UserNs = SchemaNamespace(
    schema=UserSchema,
    collection="CustomCollection",
).initialize()

# Later, adding the namespace generated from schema to our App

from some_controller import UserNs

ifmp_app.add_namespace(UserNs)

```

The crud api along with docs will be generated from the provided schema.


Bellow we have the case where we need to update the default CRUD methods provided by `MongoCrud` class.

```py

from marshmallow import Schema, fields
from licenseware.mongodata import mongodata
from licenseware.common.constants import envs
from licenseware.utils.logger import log

from licenseware.schema_namespace import SchemaNamespace, MongoCrud


# Defining our schema
class UserSchema(Schema):
    name = fields.Str(required=True)
    occupation = fields.Str(required=True)


# Overwritting mongo crud methods 
class UserOperations(MongoCrud):
    
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection
        super().__init__(schema, collection)
    
    def get_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        results = mongodata.fetch(match=query, collection=self.collection)

        return {"status": states.SUCCESS, "message": results}, 200
    
    
    def post_data(self, flask_request):

        query = UserOperations.get_query(flask_request)

        data = dict(query, **{
            "updated_at": datetime.datetime.utcnow().isoformat()}
        )

        inserted_docs = mongodata.insert(
            schema=self.schema,
            collection=self.collection,
            data=data
        )

        return inserted_docs
    
    
    def put_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        updated_docs = mongodata.update(
            schema=self.schema,
            match=query,
            new_data=dict(query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=self.collection,
            append=False
        )
        
        if updated_docs == 0:
            return {"status": states.SUCCESS, "message": "Query didn't matched any data"}, 400
        
        return {"status": states.SUCCESS, "message": ""}, 200
        
    
    def delete_data(self, flask_request):

        query = self.get_query(flask_request)

        deleted_docs = mongodata.delete(match=query, collection=self.collection)

        return deleted_docs

    
    
# A restx namespace is generated on instantiation
UserNs = SchemaNamespace(
    schema=UserSchema,
    collection="CustomCollection",
    mongo_crud_class=UserOperations,
    decorators=[]
).initialize()

# Later, adding the namespace generated from schema to our App

from some_controller import UserNs

ifmp_app.add_namespace(UserNs)


```




"""

from flask import request

# from marshmallow_jsonschema import JSONSchema
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.marshmallow_restx_converter import marshmallow_to_restx_model
from licenseware.common.validators.validate_uuid4 import validate_uuid4
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators.failsafe_decorator import failsafe
from licenseware.schema_namespace.mongo_crud import MongoCrud
from licenseware.utils.miscellaneous import http_methods, swagger_authorization_header


# Every api namespace generated with SchemaNamespace must have `tenant_id` and `updated_at` fields
class BaseSchema(Schema):
    tenant_id = fields.Str(required=True, validate=validate_uuid4)
    updated_at = fields.Str(required=False)


class SchemaNamespace:
    def __init__(
        self,
        schema: type = None,
        collection: str = None,
        methods: list = http_methods,
        decorators: list = [authorization_check],
        disable_model: bool = False,
        authorizations: dict = swagger_authorization_header,
        mongo_crud_class: type = MongoCrud,
        namespace: Namespace = None,
    ):
        self.schema = schema
        self.doc = schema.__doc__

        # Adding `tenant_id` and `updated_at` fields to received schema
        self.schema = type(
            self.schema.__name__,
            (
                self.schema,
                BaseSchema,
            ),
            {},
        )

        try:
            self.collection = self.schema.Meta.collection
        except:
            self.collection = collection or envs.MONGO_COLLECTION_DATA_NAME

        try:
            self.methods = self.schema.Meta.methods
        except:
            self.methods = methods

        self.decorators = decorators
        self.disable_model = disable_model
        self.authorizations = authorizations
        self.mongo_crud_class = mongo_crud_class
        self.namespace = namespace

        self.schema_name = self.schema.__name__
        self.name = self.schema_name.replace("Schema", "")
        self.path = "/" + self.name.lower()

    def initialize(self) -> Namespace:
        """Create restx api namespace from schema"""

        self.create_indexes()
        ns = self.create_resources()

        return ns

    def create_namespace(self) -> Namespace:
        ns = Namespace(
            name=self.name,
            path=self.path,
            description=self.doc or f"API is generated from {self.schema_name}",
            decorators=self.decorators,
            authorizations=self.authorizations,
            security=list(self.authorizations.keys()),
        )
        return ns

    def create_resources(self) -> list:

        ns = self.create_namespace()

        if self.disable_model is True:
            resource_fields = ns.model(self.name, {})
        else:
            resource_fields = marshmallow_to_restx_model(ns, self.schema)

        allowed_methods = self.methods
        data_service = self.mongo_crud_class(
            schema=self.schema, collection=self.collection
        )

        class SchemaResource(Resource):
            @failsafe(fail_code=500)
            @ns.doc(id="Make a GET request to FETCH some data")
            @ns.param("_id", "get data by id")
            @ns.response(code=200, description="A list of:", model=[resource_fields])
            @ns.response(code=404, description="Requested data not found")
            @ns.response(code=405, description="METHOD NOT ALLOWED")
            def get(self):
                if "GET" in allowed_methods:
                    return data_service.get_data(request)
                return "METHOD NOT ALLOWED", 405

            @failsafe(fail_code=500)
            @ns.doc(id="Make a POST request to INSERT some data")
            @ns.expect(resource_fields)
            @ns.response(code=400, description="Could not insert data")
            @ns.response(code=405, description="METHOD NOT ALLOWED")
            def post(self):
                if "POST" in allowed_methods:
                    return data_service.post_data(request)
                return "METHOD NOT ALLOWED", 405

            @failsafe(fail_code=500)
            @ns.doc(id="Make a PUT request to UPDATE some data")
            @ns.expect(resource_fields)
            @ns.response(code=404, description="Query had no match")
            @ns.response(code=405, description="METHOD NOT ALLOWED")
            def put(self):
                if "PUT" in allowed_methods:
                    return data_service.put_data(request)
                return "METHOD NOT ALLOWED", 405

            @failsafe(fail_code=500)
            @ns.doc(id="Make a DELETE request to DELETE some data")
            @ns.expect(resource_fields)
            @ns.response(code=404, description="Query had no match")
            @ns.response(code=405, description="METHOD NOT ALLOWED")
            def delete(self, _id=None):
                if "DELETE" in allowed_methods:
                    return data_service.delete_data(request)
                return "METHOD NOT ALLOWED", 405

        ns.add_resource(SchemaResource, "")

        if "GET" not in allowed_methods:
            ns.hide(SchemaResource.get)

        if "PUT" not in allowed_methods:
            ns.hide(SchemaResource.put)

        if "POST" not in allowed_methods:
            ns.hide(SchemaResource.post)

        if "DELETE" not in allowed_methods:
            ns.hide(SchemaResource.delete)

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
