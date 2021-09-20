import datetime
from licenseware import mongodata as m
from licenseware.utils.logger import log





class MongoCrud:
    """
        In this class we are defnining basic crud operations to mongodb
        
        All methods must use `staticmethod` decorator
        
        Create indexes will assume simple_indexes are not unique and compound_indexes are unique.
        Indexes are provided on serializer metadata (simple_indexes, compound_indexes).

    """
    
    # This vars will be filled in schema_namespace (ex: MongoCrud.schema = marshmellow_schema )
    schema = None 
    collection = None 


    @staticmethod
    def get_params(flask_request):
        params = {}
        if flask_request.args is None: return params
        params = dict(flask_request.args) or {}
        return params

    @staticmethod
    def get_payload(flask_request):
        payload = {}
        if flask_request.json is None: return payload
        if isinstance(flask_request.json, dict):
            payload = flask_request.json
        return payload

    @staticmethod
    def validate_tenant_id(tenant, params, payload):
        
        if 'tenant_id' in params:
            if params['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")
            
        if 'tenant_id' in payload:
            if payload['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")

    @staticmethod
    def get_query(flask_request):
        
        tenant = {'tenant_id': flask_request.headers.get("Tenantid")}
        
        params = MongoCrud.get_params(flask_request)
        payload = MongoCrud.get_payload(flask_request)
        
        MongoCrud.validate_tenant_id(tenant, params, payload)
        
        query = {**tenant, **params, **payload}
        
        log.info(f"Mongo CRUD Request: {query}")
        
        return query

    @staticmethod
    def get_data(flask_request):
        
        query = MongoCrud.get_query(flask_request)
        
        results = m.fetch(match=query, collection=MongoCrud.collection)

        if not results: 'Requested data not found', 404

        return results

    @staticmethod
    def post_data(flask_request):

        query = MongoCrud.get_query(flask_request)

        data = dict(query, **{
            "updated_at": datetime.datetime.utcnow().isoformat()}
        )

        inserted_docs = m.insert(
            schema=MongoCrud.schema,
            collection=MongoCrud.collection,
            data=data
        )

        if len(inserted_docs) == 0: 'Could not insert data', 400

        return "SUCCESS"


    @staticmethod
    def put_data(flask_request):
        
        query = MongoCrud.get_query(flask_request)
        
        updated_docs = m.update(
            schema=MongoCrud.schema,
            match=query,
            new_data=dict(query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=MongoCrud.collection,
            append=False
        )

        if updated_docs == 0: 'Query had no match', 404

        return "SUCCESS"


    @staticmethod
    def delete_data(flask_request):

        query = MongoCrud.get_query(flask_request)

        deleted_docs = m.delete(match=query, collection=MongoCrud.collection)

        if deleted_docs == 0: 'Query had no match', 404

        return "SUCCESS"
