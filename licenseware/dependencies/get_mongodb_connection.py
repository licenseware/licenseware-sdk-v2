# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config
from pymongo import MongoClient


def get_mongodb_connection(config: Config):
    MONGO_CONNECTION_STRING = f"mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[config.MONGO_DBNAME]
    return mongo_connection
