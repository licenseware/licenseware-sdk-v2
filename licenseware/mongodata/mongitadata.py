"""

>>> from mongita import MongitaClientDisk
>>> client = MongitaClientDisk()
>>> hello_world_db = client.hello_world_db
>>> mongoose_collection = hello_world_db.mongoose_collection
>>> mongoose_collection.insert_many([{'name': 'Meercat', 'does_not_eat': 'Snakes'},
                                     {'name': 'Yellow mongoose', 'eats': 'Termites'}])
<mongita.results.InsertManyResult object at 0x000000000>
>>> mongoose_collection.count_documents({})
2
>>> mongoose_collection.update_one({'name': 'Meercat'}, {'$set': {"weight": 2}})
<mongita.results.UpdateResult object at 00000000000>
>>> mongoose_collection.find({'weight': {'$gt': 1}})
<mongita.cursor.Cursor object at 00000000000>
>>> list(mongoose_collection.find({'weight': {'$gt': 1}}))
[{'_id': 'a1b2c3d4e5f6', 'name': 'Meercat', 'does_not_eat': 'Snakes', 'weight': 2}]
>>> mongoose_collection.delete_one({'name': 'Meercat'})
<mongita.results.DeleteResult object at 00000000000>



Abstraction and validation of inserted data in mongodb


from licenseware import mongodata
or
from licenseware import mongodata as m

Available functions:
- get_collection
- insert
- fetch
- update
- delete
- aggregate
- delete
- delete_collection
- document_count

Needs the following environment variables:
- MONGO_DATABASE_NAME
- MONGO_CONNECTION_STRING
- MONGO_COLLECTION_NAME (optional)


Pagination

For pagination make sure to include the special field `__pagination__` on `match` parameter like bellow: 

```py

results = mongodata.fetch(
    match={
            "__pagination__": {
                "limit": 20,
                "skip": 0
            }
        },
    collection=self.collection
)

```

- `limit` - is the mongo limit;
- `skip` - is the mongo skip; 


Start with `skip` value 0 and increase that value on each iteration.
If `__pagination__` is not found on match pagination will not be applied.


You can also use for pagination `limit` and `skip` paramters provided by the fetch function.


This would be the first iteration:

```py

skip = 0

results = mongodata.fetch(
    match={},
    limit = 20,
    skip = skip,
    collection=self.collection
)

skip += len(results)
```

This would be the second iteration:

```py
results = mongodata.fetch(
    match={},
    limit = 20,
    skip = skip,
    collection=self.collection
)

skip += len(results)
```

And the same is for the next iterations until `len(results)` is 0.


"""

import json
import os
from contextlib import contextmanager
from typing import Dict, Tuple, Union
from uuid import UUID

from bson.json_util import dumps
from bson.objectid import ObjectId
from mongita import MongitaClientDisk
from mongita.collection import Collection

from licenseware.utils.logger import log


def validate_data(schema, data):
    """
    Using Marshmallow schema class to validate data (dict or list of dicts)
    """

    if isinstance(data, dict):
        data = schema().load(data)

    if isinstance(data, list):
        data = schema(many=True).load(data)

    return data


def valid_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


def valid_object_id(oid_string):
    try:
        ObjectId(oid_string)
        return True
    except:
        return False


def parse_oid(oid):
    if isinstance(oid, ObjectId):
        return json.loads(dumps(oid))["$oid"]
    return oid


def parse_doc(doc):
    if not isinstance(doc, dict):
        return doc
    if not "_id" in doc:
        return doc

    return dict(doc, **{"_id": parse_oid(doc["_id"])})


def parse_match(match):
    # query_tuple - select only fields
    # distinct_key - select distinct fields

    categ = {
        "_id": None,
        "oid": None,
        "uid": None,
        "distinct_key": None,
        "query_tuple": None,
        "query": None,
    }

    if isinstance(match, dict):

        if "_id" in match:
            if valid_object_id(match["_id"]):
                match["_id"] = ObjectId(match["_id"])

        categ["query"] = match

    elif isinstance(match, str):
        if valid_uuid(match):
            match = {"_id": match}
            categ["uid"] = match
        elif valid_object_id(match):
            match = {"_id": ObjectId(match)}
            categ["oid"] = match
        else:
            categ["distinct_key"] = match

        categ["_id"] = categ["uid"] or categ["oid"]

    elif (isinstance(match, tuple) or isinstance(match, list)) and len(match) == 2:
        categ["query_tuple"] = match
    else:
        raise ValueError("Can't parse match query")

    return categ


def get_db_name(db_name):
    if db_name:
        return db_name
    default_db = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DATABASE_NAME") or "db"
    return default_db


def return_collection_name(collection):
    if collection:
        return collection
    default_collection = os.getenv("MONGO_COLLECTION_NAME") or "Data"
    return collection or default_collection


class Connect(object):
    @staticmethod
    @contextmanager
    def get_connection():
        try:
            yield MongitaClientDisk(host="./database")
        finally:
            pass


def get_collection(collection, db_name=None):
    """
    Gets the collection on which mongo CRUD operations can be performed


    """

    default_db = os.getenv("MONGO_DB_NAME") or os.getenv("MONGO_DATABASE_NAME") or "db"
    default_collection = os.getenv("MONGO_COLLECTION_NAME") or "Data"

    with Connect.get_connection() as mongo_connection:
        collection = collection or default_collection
        db_name = db_name or default_db

        if not all([db_name, collection, mongo_connection]):
            raise Exception("Can't create connection to mongo.")

        collection = mongo_connection[db_name][collection]

        return collection


def insert(schema, collection, data, db_name=None):
    """
    Insert validated documents in database.

    :schema     - Marshmallow schema class used to validate `data`
    :collection - collection name, schema name will be taken if not present
    :data       - data in dict or list of dicts format
    :db_name    - specify other db if needed, by default is MONGO_DATABASE_NAME from .env

    returns a list of ids inserted in the database in the order they were added

    """
    # log.debug("Incoming data:")
    # log.debug(data)

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        # log.debug(collection)
        if not isinstance(collection, Collection):
            return collection

        data = validate_data(schema, data)
        # log.debug("Data saved to DB")
        # log.debug(data)

        if isinstance(data, dict):
            _oid_inserted = collection.insert_one(data).inserted_id
            inserted_id = parse_oid(_oid_inserted)
            return [inserted_id]

        if isinstance(data, list):
            inserted_ids = collection.insert_many(data).inserted_ids
            return [parse_oid(oid) for oid in inserted_ids]

        raise Exception(f"Can't interpret validated data: {data}")


def get_sortli(sortdict: dict):
    if sortdict is None:
        return

    sortli = [(field, ascdesc) for field, ascdesc in sortdict.items()]

    return sortli


def fetch(
    match: Union[dict, Tuple[Dict[str, str], Dict[str, int]]],
    collection: str,
    as_list: bool = True,
    limit: int = None,
    skip: int = None,
    sortby: Dict[str, int] = None,
    db_name: str = None,
):
    """
    Get data from mongo, based on match dict or string id.

    :match      - _id as string (will return a dict)
                - mongo dict filter (will return a list of results)
                - field_name as string (will return distinct values for that field)

    :collection - collection name
    :as_list    - set as_list to false to get a generator
    :db_name    - specify other db if needed by default is MONGO_DATABASE_NAME from .env

    """

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)

    print(f"MONGO_QUERY [{db_name}.{collection_name}]: {match}")

    client = MongitaClientDisk(host="./database")
    col = client[db_name][collection_name]
    found_docs = col.find(match)
    return [parse_doc(doc) for doc in found_docs]


def aggregate(pipeline, collection, as_list=True, db_name=None):
    """
    Fetch documents based on pipeline queries.
    https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/

    :pipeline   - list of query stages
    :collection - collection name
    :as_list    - set as_list to false to get a generator
    :db_name    - specify other db if needed by default is MONGO_DATABASE_NAME from .env

    """
    log.warning("aggregate not supported by mongita...")
    return []


def _append_query(dict_: dict) -> dict:
    """
    Force append to mongo document
    """

    dict_.pop("_id", None)

    # log.warning(_id)

    q = {"$set": {}, "$addToSet": {}}
    for k in dict_:

        # if isinstance(dict_[k], str):
        #     q['$set'].update({k: dict_[k]})

        if isinstance(dict_[k], dict):
            for key in dict_[k]:
                key_ = ".".join([k, key])  # files.status
                q["$set"].update({key_: dict_[k][key]})

        elif isinstance(dict_[k], list) and dict_[k]:
            q["$addToSet"].update({k: {}})
            q["$addToSet"][k].update({"$each": dict_[k]})

        else:
            q["$set"].update({k: dict_[k]})

    if not q["$addToSet"]:
        del q["$addToSet"]
    if not q["$set"]:
        del q["$set"]

    # log_dict(q)

    return q or dict_


def update(schema, match, new_data, collection, append=False, db_name=None):
    """
    Update documents based on match query.

    :schema      - Marshmallow schema class
    :match       - id as string or dict filter query
    :new_data    - data dict which needs to be updated
    :collection  - collection name
    :append      - if true will APPEND new data to existing fields, if false will SET new data to fields
    :db_name     - specify other db if needed by default is MONGO_DATABASE_NAME from .env

    returns number of modified documents

    """
    # log.debug("Incoming data:")
    # log.debug(new_data)

    new_data = validate_data(schema, new_data)

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)

    print(f"MONGO_QUERY [{db_name}.{collection_name}]: {match}")

    client = MongitaClientDisk(host="./database")
    col = client[db_name][collection_name]

    matched_data = col.find_one(filter=match)
    if matched_data is None:
        col.insert_one(new_data)
        return 1

    new_full_data = {**matched_data, **new_data} if matched_data else new_data

    updated_docs_nbr = col.replace_one(
        filter=match, replacement=new_full_data
    ).modified_count

    return updated_docs_nbr


def delete(match, collection, db_name=None):
    """

    Delete documents based on match query.

    :match       - id as string or dict filter query,
    :collection  - collection name
    :db_name     - specify other db if needed by default is MONGO_DATABASE_NAME from .env

    returns number of deleted documents



    """

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)

    print(f"MONGO_QUERY [{db_name}.{collection_name}]: {match}")

    client = MongitaClientDisk(host="./database")
    col = client[db_name][collection_name]

    col.delete_many(match)


def delete_collection(collection, db_name=None):
    """
    Delete a collection from the database.
    """
    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        if not isinstance(collection, Collection):
            return collection

        res = collection.drop()
        return 1 if res is None else 0


def distinct(match, key, collection, db_name=None):
    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        return collection.distinct(key, match)


def document_count(match, collection, db_name=None):
    """
    Delete a collection from the database.
    """
    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        if not isinstance(collection, Collection):
            return collection

        return collection.count_documents(filter=match)


# These are just mock funcs for mongita (not used yet)
def create_timeseries_collection(
    collection_name: str, db_name: str = None, timeseries_config: dict = None
):
    db_name = get_db_name(db_name=db_name)
    with Connect.get_connection() as mongo_connection:
        db_conn = mongo_connection[db_name]
        try:
            db_conn.create_collection(
                name=collection_name, timeseries=timeseries_config
            )
            log.info(f"Successfully created collection {collection_name}.")
        except Exception as err:
            if "already exists" in err._message:
                log.info(f"Collection {collection_name} already exists, skipping.")
            else:
                log.error(f"Could not create collection {collection_name}")


def create_collection(
    collection_name: str, db_name: str = None, timeseries_config: dict = None
):
    # TODO generalize this overall for mongo dbs and collections to add indexes and any other config.
    db_name = get_db_name(db_name=db_name)
    if timeseries_config:
        return create_timeseries_collection(
            collection_name=collection_name,
            timeseries_config=timeseries_config,
            db_name=db_name,
        )
    with Connect.get_connection() as mongo_connection:
        db_conn = mongo_connection[db_name]
        try:
            db_conn.create_collection(
                name=collection_name,
            )
            log.info(f"Successfully created collection {collection_name}.")
        except Exception as err:
            if "already exists" in err._message:
                log.info(f"Collection {collection_name} already exists, skipping.")
            else:
                log.error(f"Could not create collection {collection_name}")
