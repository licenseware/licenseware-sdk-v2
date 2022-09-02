"""

Function `collection` is a context manager which can be used as folows:

```py

from licensware.mongodata import collection


with collection("CollectionName", MarshmallowSchema, data) as col:
    col.find({}) #any pymongo collection functions


```

`MarshmallowSchema` will validate provided `data` provided before inserting it in mongo


"""

from contextlib import contextmanager

from marshmallow import Schema
from pymongo import MongoClient

from licenseware.common.constants import envs


@contextmanager
def collection(collection_name: str, schema: Schema = None, data: any = None):

    if schema and data:

        if isinstance(data, dict):
            data = schema().load(data)

        if isinstance(data, list):
            data = schema(many=True).load(data)

    with MongoClient(envs.MONGO_CONNECTION_STRING) as conn:
        col = conn[envs.MONGO_DATABASE_NAME][collection_name]
        try:
            yield col
        finally:
            conn.close()
