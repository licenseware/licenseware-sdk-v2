import datetime
from flask import Request
from marshmallow.schema import Schema
from licenseware import mongodata as m
from licenseware.utils.logger import log


class MongoCrud:
    """
        In this class we are defining basic crud operations to mongodb
        
        All methods must use `staticmethod` decorator
        
        Create indexes will assume simple_indexes are not unique and compound_indexes are unique.
        Indexes are provided on serializer metadata (simple_indexes, compound_indexes).

    """

    def __init__(self, schema: Schema, collection: str, get_pipeline: list = []):

        self.schema = schema
        self.collection = collection
        self.get_pipeline = get_pipeline

    def get_params(self, flask_request: Request):
        params = {}
        if flask_request.args is None: return params
        params = dict(flask_request.args) or {}
        return params

    def get_payload(self, flask_request: Request):
        payload = {}
        if flask_request.json is None: return payload
        if isinstance(flask_request.json, dict):
            payload = flask_request.json
        return payload

    def validate_tenant_id(self, tenant, params, payload):

        if 'tenant_id' in params:
            if params['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")

        if 'tenant_id' in payload:
            if payload['tenant_id'] != tenant['tenant_id']:
                raise Exception("The 'tenant_id' provided in query parameter is not the same as the one from headers")

    def get_query(self, flask_request: Request):

        tenant = {'tenant_id': flask_request.headers.get("Tenantid")}

        params = self.get_params(flask_request)
        payload = self.get_payload(flask_request)

        self.validate_tenant_id(tenant, params, payload)

        query = {**tenant, **params, **payload}

        log.info(f"Mongo CRUD Request: {query} (schema: {self.schema.__name__}, collection: {self.collection})")

        return query

    def get_data(self, flask_request: Request):

        tenant = {'tenant_id': flask_request.headers.get("Tenantid")}
        params = self.get_params(flask_request)
        if 'foreign_key' not in params:
            if self.get_pipeline:
                self.get_pipeline.insert(0, {"$match": tenant})
                log.warning(self.get_pipeline)
                result = m.aggregate(self.get_pipeline, collection=self.collection)
                log.warning(result)
                return result
            result = m.fetch(match=tenant, collection=self.collection)
            log.warning(result)
            return result
        result = m.distinct(match=tenant, key=params['foreign_key'], collection=self.collection)
        log.warning(result)
        return result

        # query = self.get_query(flask_request)

        # results = m.fetch(match=query, collection=self.collection)

        # if len(results) == 0: return  'Requested data not found', 404

        # return results

    def post_data(self, flask_request: Request):

        query = self.get_query(flask_request)

        data = dict(query, **{
            "updated_at": datetime.datetime.utcnow().isoformat()}
                    )

        inserted_docs = m.insert(
            schema=self.schema,
            collection=self.collection,
            data=data
        )

        if len(inserted_docs) == 0: return 'Could not insert data', 400

        return "SUCCESS"

    def put_data(self, flask_request: Request):

        query = self.get_query(flask_request)

        updated_docs = m.update(
            schema=self.schema,
            match=query,
            new_data=dict(query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=self.collection,
            append=False
        )

        if updated_docs == 0: return 'Query had no match', 404

        return "SUCCESS"

    def delete_data(self, flask_request: Request):

        query = self.get_query(flask_request)

        deleted_docs = m.delete(match=query, collection=self.collection)

        if deleted_docs == 0: return 'Query had no match', 404

        return "SUCCESS"
