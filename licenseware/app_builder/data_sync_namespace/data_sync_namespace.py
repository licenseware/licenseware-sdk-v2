from flask_restx import Namespace
from marshmallow import Schema

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import machine_check
from licenseware.mongodata import mongodata
from licenseware.schema_namespace import MongoCrud, SchemaNamespace


class MongoDataSync(MongoCrud):
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection

    def get_data(self, flask_request):
        tenant = flask_request.headers.get("TenantId")
        if not tenant:
            raise Exception("TenantId header is required")

        query = self.get_query(flask_request)
        coll = mongodata.get_collection(self.collection)
        return list(coll.find(query))


class DataSyncRoute(SchemaNamespace):

    """
    Create a data sync endpoint with machine authorization.
    Receives a schema and a collection name as optional (it will use mongo data collection by default)
    Only implements the get_data functionality of MongoCrud (read-only)
    Requires a TenantId header along with the machine authorization

    """

    def __init__(self, ns: Namespace, schema: Schema, collection_name: str = None):
        self.schema = schema
        self.collection = collection_name or envs.MONGO_COLLECTION_DATA_NAME
        self.methods = ["GET"]
        self.decorators = [machine_check]
        self.mongo_crud_class = MongoDataSync
        self.namespace = ns
        super().__init__(**vars(self))


def get_data_sync_namespace(ns: Namespace, data_sync_schema: Schema):
    class DataSyncSchema(data_sync_schema):
        ...

    collection_name = None
    if hasattr(data_sync_schema, "Meta"):
        if hasattr(data_sync_schema.Meta, "mongo_collection_name"):
            collection_name = data_sync_schema.Meta.mongo_collection_name

    ns = DataSyncRoute(ns, DataSyncSchema, collection_name).initialize()

    return ns
