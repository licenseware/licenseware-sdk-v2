import uuid
import datetime
import logging
import licenseware.mongodata as m
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

    request_obj = None  # This will be updated when a http request is made (see MongoRequest)

    @property
    def params(self):
        params = {}
        if self.request_obj.args is None: return params
        params = dict(self.request_obj.args) or {}
        params.pop('tenant_id', None)
        return params

    @property
    def payload(self):
        payload = {}
        if self.request_obj.json is None: return payload
        if isinstance(self.request_obj.json, dict):
            payload = self.request_obj.json
            payload.pop('tenant_id', None)

        return payload

    @property
    def query(self):
        tenant = {'tenant_id': self.request_obj.headers.get("TenantId")}
        query = {**tenant, **self.params, **self.payload}
        logging.warning(f"CRUD Request: {query}")
        return query

    def create_indexes(self):
        coll = m.get_collection(self.collection)
        try:
            for i in self.schema.Meta.simple_indexes:
                coll.create_index(i)
        except AttributeError:
            logging.info("No simple indexes declared")
        try:
            for ci in self.schema.Meta.compound_indexes:
                col_list = [(ci_m, 1) for ci_m in ci]
                coll.create_index(col_list, unique=True)
        except AttributeError:
            logging.info("No compound indexes declared")

    def fetch_data(self, request_obj):
        self.request_obj = request_obj

        results = m.fetch(match=self.query, collection=self.collection)

        if isinstance(results, str):
            abort(500, reason=results)

        if not results:
            abort(404, reason='Requested data not found')

        return results

    def update_data(self, request_obj):
        self.request_obj = request_obj

        updated_docs = m.update(
            schema=self.schema,
            match=self.query,
            new_data=dict(self.query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=self.collection,
            append=False
        )

        if updated_docs == 0:
            abort(404, reason='Query had no match')

        if isinstance(updated_docs, str):
            abort(500, reason=updated_docs)

        return "SUCCESS"

    def insert_data(self, request_obj):
        self.request_obj = request_obj

        data = dict(self.query, **{
            "_id": str(uuid.uuid4()),
            "updated_at": datetime.datetime.utcnow().isoformat()}
                    )

        inserted_docs = m.insert(
            schema=self.schema,
            collection=self.collection,
            data=data
        )

        if len(inserted_docs) == 0:
            abort(404, reason='Could not insert data')

        if isinstance(inserted_docs, str):
            abort(500, reason=inserted_docs)

        return "SUCCESS"

    def delete_data(self, request_obj):
        self.request_obj = request_obj

        deleted_docs = m.delete(match=self.query, collection=self.collection)

        if deleted_docs == 0:
            abort(404, reason='Query had no match')

        if isinstance(deleted_docs, str):
            abort(500, reason=deleted_docs)

        return "SUCCESS"
