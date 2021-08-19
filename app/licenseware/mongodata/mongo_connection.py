"""
Here we are creating a connection to mongo database using 
MONGO_CONNECTION_STRING from environment variables.

We are also creating the default collections (if not present) in the database

We are using MongoClient because it's thread and fork safe.

Object `db` is available for import (has all pymongo functions)


TODO count number of connections, use context manager for client connection

"""

from pymongo import MongoClient
from app.licenseware.common.constants import envs

client = MongoClient(envs.MONGO_CONNECTION_STRING)
# Raise error if connection is not established
client.admin.command('ping')
# Get database on which we can create and modify collections
db = client[envs.MONGO_DATABASE_NAME]

# Creating default collections
existing_collections = db.list_collections()
if len(list(existing_collections)) == 0:
    db.create_collection(envs.MONGO_COLLECTION_DATA_NAME)
    db.create_collection(envs.MONGO_COLLECTION_ANALYSIS_NAME)
    db.create_collection(envs.MONGO_COLLECTION_UTILIZATION_NAME)
    
