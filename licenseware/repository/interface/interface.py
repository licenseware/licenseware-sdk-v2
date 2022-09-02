from abc import ABCMeta, abstractmethod
from typing import List, Union

from marshmallow import Schema


class RepositoryInterface(metaclass=ABCMeta):
    # db_url param should be provided on constructor
    db_url = None

    @classmethod
    def __subclasshook__(cls, subclass):
        # Ensure that all methods and attrs are provided

        return (
            hasattr(subclass, "db_url")
            and isinstance(subclass.db_url, str)
            or isinstance(subclass.db_url, str)
            and hasattr(subclass, "fetch")
            and callable(subclass.fetch)
            and hasattr(subclass, "fetch_one")
            and callable(subclass.fetch_one)
            and hasattr(subclass, "fetch_by_id")
            and callable(subclass.fetch_by_id)
            and hasattr(subclass, "fetch_many")
            and callable(subclass.fetch_many)
            and hasattr(subclass, "insert")
            and callable(subclass.insert)
            and hasattr(subclass, "insert_one")
            and callable(subclass.insert_one)
            and hasattr(subclass, "insert_with_id")
            and callable(subclass.insert_with_id)
            and hasattr(subclass, "insert_many")
            and callable(subclass.insert_many)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            and hasattr(subclass, "update_one")
            and callable(subclass.update_one)
            and hasattr(subclass, "update_on_id")
            and callable(subclass.update_on_id)
            and hasattr(subclass, "update_many")
            and callable(subclass.update_many)
            and hasattr(subclass, "delete")
            and callable(subclass.delete)
            and hasattr(subclass, "delete_one")
            and callable(subclass.delete_one)
            and hasattr(subclass, "delete_by_id")
            and callable(subclass.delete_by_id)
            and hasattr(subclass, "delete_many")
            and callable(subclass.delete_many)
            and hasattr(subclass, "count")
            and callable(subclass.count)
            # Fail
            or NotImplemented
        )

    # Fetching data

    @abstractmethod
    def fetch(
        self,
        schema_name: str,
        id: str = None,
        first: bool = False,
        limit: int = None,
        skip: int = None,
        **filters
    ) -> List[dict]:
        """ """
        raise NotImplementedError

    @abstractmethod
    def fetch_one(self, schema_name: str, **filters) -> dict:
        """Get first item match"""
        return self.fetch(schema_name, first=True, **filters)

    @abstractmethod
    def fetch_by_id(self, schema_name: str, id: str) -> dict:
        """Get first item match by id"""
        return self.fetch(schema_name, first=True, id=id)

    @abstractmethod
    def fetch_many(self, schema_name: str, **filters) -> List[dict]:
        """Get all items that matched"""
        return self.fetch(schema_name, **filters)

        # Inserting new data

    @abstractmethod
    def insert(self, schema: Schema, data: Union[dict, List[dict]]) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def insert_one(self, schema: Schema, data: dict = None, **data_kwargs) -> any:
        """Insert dict to db"""
        return self.insert(schema, data or data_kwargs)

    @abstractmethod
    def insert_with_id(
        self, schema: Schema, id: Union[str, int], data: dict = None, **data_kwargs
    ) -> any:
        """Insert dict with a specific 'id'"""
        raise NotImplementedError

    @abstractmethod
    def insert_many(
        self, schema: Schema, data: List[dict], validate_percentage: float = 1.0
    ) -> any:
        """
        TODO `validate_percentage`: what percentage of the list of data provided should be validated (0.5 is 50%)
        """
        return self.insert(schema, data)

    # Updating existing data

    @abstractmethod
    def update(
        self,
        schema_name: str,
        filters: dict,
        data: Union[dict, List[dict]],
        first: bool = False,
    ) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def update_one(
        self, filters: dict, data: dict, append: bool = False, schema: Schema = None
    ) -> dict:
        """ """
        raise NotImplementedError

    @abstractmethod
    def update_on_id(self, schema_name: str, id: Union[str, int], data: dict) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def update_many(
        self,
        schema_name: str,
        filters: dict,
        data: List[dict],
        validate_percentage: float = 1.0,
    ) -> any:
        """
        `validate_percentage`: what percentage of the list of data provided should be validated (0.5 is 50% of items in list)
        """
        raise NotImplementedError

    # Deleting existing data

    @abstractmethod
    def delete(self, schema_name: str, filters: dict, first: bool = False) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, schema_name: str, **filters) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(elf, schema_name: str, id: str) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def delete_many(self, schema_name: str, **filters) -> any:
        """ """
        raise NotImplementedError

    @abstractmethod
    def count(self, schema_name: str, **filters) -> any:
        """ """
        raise NotImplementedError
