from marshmallow import Schema

from licenseware.repository.interface import RepositoryInterface


class MongoRepository(RepositoryInterface):
    def __init__(self, db_url: str, schema: Schema):
        self.db_url = db_url
        self.schema = schema


# from pymongo import MongoClient
# from marshmallow import Schema
# from contextlib import contextmanager


# MONGO_DATABASE_NAME = 'db'
# MONGO_CONNECTION_STRING = "mongodb://localhost:27017/db"


# @contextmanager
# def collection(collection_name:str, schema: Schema = None, data:any = None):

#     if schema and data:

#         if isinstance(data, dict):
#             data = schema().load(data)

#         if isinstance(data, list):
#             data = schema(many=True).load(data)


#     with MongoClient(MONGO_CONNECTION_STRING) as conn:
#         col = conn[MONGO_DATABASE_NAME][collection_name]
#         try:
#             yield col
#         finally:
#             conn.close()
