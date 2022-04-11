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

import os
import json
from typing import Union, Tuple, List, Dict
from uuid import UUID
from mongita import MongitaClientDisk
from mongita.collection import Collection
from bson.json_util import dumps
from bson.objectid import ObjectId
from mongita.write_concern import WriteConcern
from mongita.read_concern import ReadConcern

from licenseware.utils.logger import log


from contextlib import contextmanager



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
        return json.loads(dumps(oid))['$oid']
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
        '_id': None,
        'oid': None,
        'uid': None,
        'distinct_key': None,
        'query_tuple': None,
        'query': None
    }

    if isinstance(match, dict):

        if '_id' in match:
            if valid_object_id(match['_id']):
                match['_id'] = ObjectId(match['_id'])

        categ['query'] = match

    elif isinstance(match, str):
        if valid_uuid(match):
            match = {"_id": match}
            categ['uid'] = match
        elif valid_object_id(match):
            match = {"_id": ObjectId(match)}
            categ['oid'] = match
        else:
            categ['distinct_key'] = match

        categ['_id'] = categ['uid'] or categ['oid']

    elif (isinstance(match, tuple) or isinstance(match, list)) and len(match) == 2:
        categ['query_tuple'] = match
    else:
        raise ValueError("Can't parse match query")

    return categ


def get_db_name(db_name):
    if db_name:
        return db_name
    default_db = os.getenv("MONGO_DB_NAME") or os.getenv(
        "MONGO_DATABASE_NAME") or "db"
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

    default_db = os.getenv("MONGO_DB_NAME") or os.getenv(
        "MONGO_DATABASE_NAME") or "db"
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
    if sortdict is None: return

    sortli = [
        (field, ascdesc)
        for field, ascdesc in sortdict.items()
    ]

    return sortli


def fetch(match: Union[dict, Tuple[Dict[str, str], Dict[str, int]]], collection: str, as_list: bool = True, limit: int = None, skip: int = None,
          sortby: Dict[str, int] = None, db_name: str = None):
    """
        Get data from mongo, based on match dict or string id.

        :match      - _id as string (will return a dict)
                    - mongo dict filter (will return a list of results)
                    - field_name as string (will return distinct values for that field)

        :collection - collection name
        :as_list    - set as_list to false to get a generator
        :db_name    - specify other db if needed by default is MONGO_DATABASE_NAME from .env

    """

    # TODO - needs refatoring (to much going on)

    pagination = None
    if isinstance(match, dict):
        pagination = match.pop("__pagination__", None)

    match = parse_match(match)
    sortbylist = get_sortli(sortby)

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)

    log.info(f"MONGO_QUERY [{db_name}.{collection_name}]: {match}")

    with Connect.get_connection() as mongo_connection:
        collection: MongitaClientDisk = mongo_connection[db_name][collection_name]
        # log.debug(collection)
        if not isinstance(collection, Collection):
            return collection

        if match['_id']:
            found_docs = collection.find(match['_id']) if sortbylist is None else collection.find(match['_id']).sort(
                sortbylist)
            doc = []
            if found_docs: doc = list(found_docs)[0]
            if match['oid']: doc = parse_doc(doc)
            return doc

        if match['distinct_key']:
            found_docs = collection.distinct(match['distinct_key'])

        elif match['query_tuple']:

            if pagination:

                if sortbylist is None:

                    found_docs = collection \
                        .find(*match['query_tuple']) \
                        .skip(pagination['skip']) \
                        .limit(pagination['limit'])

                else:
                    found_docs = collection \
                        .find(*match['query_tuple']) \
                        .sort(sortbylist) \
                        .skip(pagination['skip']) \
                        .limit(pagination['limit'])

            elif limit is not None and skip is not None:

                if sortbylist is None:
                    found_docs = collection \
                        .find(*match['query_tuple']) \
                        .skip(skip) \
                        .limit(limit)
                else:
                    found_docs = collection \
                        .find(*match['query_tuple']) \
                        .sort(sortbylist) \
                        .skip(skip) \
                        .limit(limit)

            else:
                if sortbylist is None:
                    found_docs = collection.find(*match['query_tuple'])
                else:
                    found_docs = collection.find(*match['query_tuple']).sort(sortbylist)

        else:

            if pagination:

                if sortbylist is None:

                    found_docs = collection \
                        .find(match['query']) \
                        .skip(pagination['skip']) \
                        .limit(pagination['limit'])

                else:

                    found_docs = collection \
                        .find(match['query']) \
                        .sort(sortbylist) \
                        .skip(pagination['skip']) \
                        .limit(pagination['limit'])

            elif limit is not None and skip is not None:

                if sortbylist is None:

                    found_docs = collection \
                        .find(match['query']) \
                        .skip(skip) \
                        .limit(limit)

                else:

                    found_docs = collection \
                        .find(match['query']) \
                        .sort(sortbylist) \
                        .skip(skip) \
                        .limit(limit)

            else:

                if sortbylist is None:
                    found_docs = collection.find(match['query'])
                else:
                    found_docs = collection.find(match['query']).sort(sortbylist)

        if as_list:
            return [parse_doc(doc) for doc in found_docs]

        return (parse_doc(doc) for doc in found_docs)


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

    _id = dict_.pop("_id", None)

    # log.warning(_id)

    q = {'$set': {}, '$addToSet': {}}
    for k in dict_:

        # if isinstance(dict_[k], str):
        #     q['$set'].update({k: dict_[k]})

        if isinstance(dict_[k], dict):
            for key in dict_[k]:
                key_ = ".".join([k, key])  # files.status
                q['$set'].update({key_: dict_[k][key]})

        elif isinstance(dict_[k], list) and dict_[k]:
            q['$addToSet'].update({k: {}})
            q['$addToSet'][k].update({"$each": dict_[k]})

        else:
            q['$set'].update({k: dict_[k]})

    if not q['$addToSet']:
        del q['$addToSet']
    if not q['$set']:
        del q['$set']

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

    db_name = get_db_name(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        match = parse_match(match)
        match = match['query'] or match['_id']
        if not match:
            match = match['_id'] = match['distinct_key']

        new_data = validate_data(schema, new_data)
        # log.debug("Data saved to DB")
        # log.debug(new_data)

        _filter = {"_id": match["_id"]} if "_id" in match else match

        log.info(f"MONGO_QUERY [{db_name}.{collection_name}]: {_filter}")

        updated_docs_nbr = collection.replace_one(
            filter=_filter,
            replacement=new_data
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

    log.info(f"MONGO_QUERY [{db_name}.{collection_name}]: {match}")

    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        match = parse_match(match)

        if not isinstance(collection, Collection):
            return collection

        deleted_docs_nbr = collection.delete_many(
            filter=match['query'] or match['_id'],
        ).deleted_count

        return deleted_docs_nbr


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
