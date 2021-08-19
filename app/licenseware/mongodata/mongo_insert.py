from marshmallow import Schema
from .mongo_connection import db
from app.licenseware.common.validators.schema_validator import validate_data


def insert(*, collection:str, data:dict, schema:Schema = None) -> list:
    """
        Insert validated documents in database.

        :schema     - Marshmallow schema class used to validate `data`
        :collection - collection name (table_name)
        :data       - data in dict or list of dicts format
        
        returns a list of ids inserted in the database in the order they were added
        If something fails will return a string with the error message.
    """
    
    
    db[collection]
    
    
    
    
        data = validate_data(schema, data)
        if isinstance(data, str):
            return data

        try:

            if isinstance(data, dict):
                # _oid_inserted = collection.with_options(
                #     write_concern=WriteConcern("majority")).insert_one(data).inserted_id
                _oid_inserted = collection.insert_one(data).inserted_id
                inserted_id = parse_oid(_oid_inserted)
                return [inserted_id]

            if isinstance(data, list):
                inserted_ids = collection.with_options(
                    write_concern=WriteConcern("majority")).insert_many(data).inserted_ids
                return [parse_oid(oid) for oid in inserted_ids]

            raise Exception(f"Can't interpret validated data: {data}")
        except DuplicateKeyError:
            raise Exception(f"Key already exists")





@failsafe
def insert(schema, collection, data, db_name=None):
    """
        Insert validated documents in database.

        :schema     - Marshmallow schema class used to validate `data`
        :collection - collection name, schema name will be taken if not present
        :data       - data in dict or list of dicts format
        :db_name    - specify other db if needed, by default is MONGO_DATABASE_NAME from .env

        returns a list of ids inserted in the database in the order they were added
        If something fails will return a string with the error message.
    """
    db_name = return_db(db_name)
    collection_name = return_collection_name(collection)
    with Connect.get_connection() as mongo_connection:
        collection = mongo_connection[db_name][collection_name]
        if not isinstance(collection, Collection):
            return collection

        data = validate_data(schema, data)
        if isinstance(data, str):
            return data

        try:

            if isinstance(data, dict):
                # _oid_inserted = collection.with_options(
                #     write_concern=WriteConcern("majority")).insert_one(data).inserted_id
                _oid_inserted = collection.insert_one(data).inserted_id
                inserted_id = parse_oid(_oid_inserted)
                return [inserted_id]

            if isinstance(data, list):
                inserted_ids = collection.with_options(
                    write_concern=WriteConcern("majority")).insert_many(data).inserted_ids
                return [parse_oid(oid) for oid in inserted_ids]

            raise Exception(f"Can't interpret validated data: {data}")
        except DuplicateKeyError:
            raise Exception(f"Key already exists")

