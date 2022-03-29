from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import machine_check
from licenseware.schema_namespace import MongoCrud, SchemaNamespace
from licenseware.mongodata import mongodata
from marshmallow import Schema, fields, validate


class MongoDataSync(MongoCrud):
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection

    def get_data(self, flask_request):
        tenant = flask_request.headers.get("Tenantid")
        if not tenant:
            raise Exception("TenantId header is required")

        query = self.get_query(flask_request)
        coll = mongodata.get_collection(self.collection)
        return coll.find(query)


class DataSyncRoute(SchemaNamespace):

    """
        Create a data sync endpoint with machine authorization.
        Receives a serializer and a collection name as optional (it will use mongo data collection by default)
        Only implements the get_data functionality of MongoCrud (read-only)
        Requires a TenantId header along with the machine authorization
    """

    def __init__(self, serializer, collection_name=envs.MONGO_COLLECTION_DATA_NAME):
        self.collection_name = collection_name
        self.schema=serializer
        self.collection=collection_name
        self.methods=["GET"]
        self.decorators=[machine_check]
        self.mongo_crud_class=MongoDataSync

    