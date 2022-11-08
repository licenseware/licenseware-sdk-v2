from typing import Callable, List, Tuple, Union

from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from licenseware.repository.repository_interface import RepositoryInterface
from licenseware.utils.logger import log

from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(
        self,
        db_connection: Database,
        collection: str = None,
        data_validator: Callable = None,
    ):
        self.db_connection = db_connection
        self.collection = collection
        self.data_validator = data_validator

    def _setid(self, data: dict):
        if data is None:  # pragma no cover
            return {}
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def _setids(self, cursor: Cursor):

        getid = (
            lambda doc: {"_id": utils.get_object_id_str(doc["_id"])}
            if "_id" in doc
            else {}
        )

        return [{**doc, **getid(doc)} for doc in cursor]

    def _get_collection(self, collection: str) -> Collection:
        collection = collection or self.collection
        assert collection is not None
        col: Collection = self.db_connection[collection]
        return col

    def _get_validated_data(self, data, data_validator: Callable):

        if (
            data_validator == "ignore" or self.data_validator == "ignore"
        ):  # pragma no cover
            return data

        if data_validator is None and self.data_validator is None:
            log.warning("Attention! No data validator function provided!")
            return data

        if data_validator is not None:
            return data_validator(data)

        if self.data_validator is not None:  # pragma no cover
            return self.data_validator(data)

        return data  # pragma no cover

    def _parse_filters(self, filters: dict):
        if filters is None:
            return
        if "_id" in filters:
            return {**filters, **{"_id": utils.get_object_id(filters["_id"])}}
        return filters

    # RAW

    def execute_query(self, query: List[dict], collection: str = None) -> List[dict]:
        col = self._get_collection(collection)
        cursor = col.aggregate(pipeline=query, allowDiskUse=True)
        return self._setids(cursor)

    # finding data

    def find_one(self, filters: dict, collection: str = None) -> dict:
        col = self._get_collection(collection)
        data = col.find_one(self._parse_filters(filters))
        return self._setid(data)

    def find_by_id(self, id: str, collection: str = None) -> dict:
        col = self._get_collection(collection)
        data = col.find_one({"_id": utils.get_object_id(id)})
        return self._setid(data)

    def find_many(
        self,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
        collection: str = None,
    ) -> List[dict]:

        col = self._get_collection(collection)
        cursor = col.find(
            filter=self._parse_filters(filters),
            skip=skip,
            limit=limit,
            sort=sort,
        )
        return self._setids(cursor)

    def distinct(
        self,
        field: str,
        filters: dict = None,
        collection: str = None,
    ) -> List[str]:
        col = self._get_collection(collection)
        data = col.distinct(key=field, filter=self._parse_filters(filters))
        return data

    def count(
        self,
        filters: dict = None,
        collection: str = None,
    ) -> int:
        col = self._get_collection(collection)
        if filters is None:
            filters = {}

        return col.count_documents(filter=self._parse_filters(filters))

    # Inserting new data

    def insert_one(
        self,
        data: dict,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        col.insert_one(data)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def insert_with_id(
        self,
        id: Union[str, int],
        data: dict,
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data["_id"] = utils.get_object_id(id)
        if overwrite:
            col.delete_one({"_id": data["_id"]})
        col.insert_one(data)
        return data

    def insert_many(
        self,
        data: List[dict],
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> List[dict]:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        if overwrite:  # pragma no cover
            col.delete_many(
                {"_id": {"$in": [utils.get_object_id(d["_id"]) for d in data]}}
            )
        col.insert_many(data)
        return self._setids(data)

    # Updating existing data

    def update_one(
        self,
        filters: dict,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_update(
            filter=self._parse_filters(filters),
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
            return_document=True,
        )
        return self._setid(data)

    def update_on_id(
        self,
        id: str,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_update(
            filter={"_id": utils.get_object_id(id)},
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
            return_document=True,
        )
        return self._setid(data)

    def update_many(
        self,
        filters: dict,
        data: List[dict],
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> int:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        return col.update_many(
            filter=self._parse_filters(filters),
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
        ).matched_count

    def replace_one(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_replace(
            filter=self._parse_filters(filters),
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_on_id(
        self,
        id: str,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_replace(
            filter={"_id": utils.get_object_id(id)},
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_many(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> int:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        deleted_count = col.delete_many(filter=filters).deleted_count
        modified_count = col.update_many(
            filter=self._parse_filters(filters),
            update=utils.add_update_operators(data, False),
            upsert=upsert,
        ).modified_count
        return deleted_count or modified_count or int(upsert)

    # Deleting existing data

    def delete_one(self, filters: dict, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_one(filter=self._parse_filters(filters)).deleted_count

    def delete_on_id(self, id: str, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_one(filter={"_id": utils.get_object_id(id)}).deleted_count

    def delete_many(self, filters: dict, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_many(filter=self._parse_filters(filters)).deleted_count
