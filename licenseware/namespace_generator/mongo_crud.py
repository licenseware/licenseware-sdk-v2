import datetime
from licenseware import mongodata as m
from licenseware.utils.logger import log
from flask_restx import abort


# TODO
# ONE TO ONE
# ONE TO MANY
# MANY TO MANY
# All Child objects should be deleted when their owning Parent is deleted.


class MongoCrud:
    """
        This class provides get, post, put, delete http methods.

        Needs a TenantId in the request header.
        Decorator authorization_check makes sure that TenantId and auth_token are provided

        Query params are taken from request.args, '_id' parameter is just for swagger documentation.

        Create indexes will assume simple_indexes are not unique and compound_indexes are unique.
        Indexes are provided on serializer metadata (simple_indexes, compound_indexes).

    """

    def get_params(self, request_obj):
        params = {}
        if request_obj.args is None: return params
        params = dict(request_obj.args) or {}
        return params

    def get_payload(self, request_obj):
        payload = {}
        if request_obj.json is None: return payload
        if isinstance(request_obj.json, dict):
            payload = request_obj.json
        return payload


    def validate_tenant_id(self, tenant, params, payload):
        
        if 'tenant_id' in params:
            if params['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")
            
        if 'tenant_id' in payload:
            if payload['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")


    def get_query(self, request_obj):
        
        tenant = {'tenant_id': request_obj.headers.get("Tenantid")}
        
        params = self.get_params(request_obj)
        payload = self.get_payload(request_obj)
        
        self.validate_tenant_id(tenant, params, payload)
        
        query = {**tenant, **params, **payload}
        
        log.info(f"Mongo CRUD Request: {query}")
        
        return query


    def get_data(self, request_obj):
        
        query = self.get_query(request_obj)
        
        results = m.fetch(match=query, collection=self.collection)

        if not results: abort(404, reason='Requested data not found')

        return results


    def post_data(self, request_obj):

        query = self.get_query(request_obj)

        data = dict(query, **{
            "updated_at": datetime.datetime.utcnow().isoformat()}
        )

        inserted_docs = m.insert(
            schema=self.schema,
            collection=self.collection,
            data=data
        )

        if len(inserted_docs) == 0: abort(404, reason='Could not insert data')

        return "SUCCESS"


    def put_data(self, request_obj):
        
        query = self.get_query(request_obj)
        
        updated_docs = m.update(
            schema=self.schema,
            match=query,
            new_data=dict(self.query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=self.collection,
            append=False
        )

        if updated_docs == 0: abort(404, reason='Query had no match')

        return "SUCCESS"


    def delete_data(self, request_obj):

        query = self.get_query(request_obj)

        deleted_docs = m.delete(match=query, collection=self.collection)

        if deleted_docs == 0: abort(404, reason='Query had no match')

        return "SUCCESS"
