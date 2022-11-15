from abc import ABCMeta, abstractmethod
from typing import Callable, List, Tuple, Union


class RepositoryInterface(metaclass=ABCMeta):  # pragma no cover

    # RAW

    @abstractmethod
    def execute_query(self, query: List[dict], collection: str = None) -> List[dict]:
        ...

    # finding data

    @abstractmethod
    def find_one(self, filters: dict, collection: str = None) -> dict:
        ...

    @abstractmethod
    def find_by_id(self, id: str, collection: str = None) -> dict:
        ...

    @abstractmethod
    def find_many(
        self,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
        collection: str = None,
    ) -> List[dict]:
        ...

    @abstractmethod
    def distinct(
        self,
        field: str,
        filters: dict = None,
        collection: str = None,
    ) -> List[str]:
        ...

    @abstractmethod
    def count(
        self,
        filters: dict = None,
        collection: str = None,
    ) -> int:
        ...

    # Inserting new data

    @abstractmethod
    def insert_one(
        self,
        data: dict,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        ...

    @abstractmethod
    def insert_with_id(
        self,
        id: Union[str, int],
        data: dict,
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        ...

    @abstractmethod
    def insert_many(
        self,
        data: List[dict],
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> List[dict]:
        ...

    # Updating existing data

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def replace_one(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        ...

    @abstractmethod
    def replace_on_id(
        self,
        id: str,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        ...

    @abstractmethod
    def replace_many(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> int:
        ...

    # Deleting existing data

    @abstractmethod
    def delete_one(self, filters: dict, collection: str = None) -> int:
        ...

    @abstractmethod
    def delete_on_id(self, id: str, collection: str = None) -> int:
        ...

    @abstractmethod
    def delete_many(self, filters: dict, collection: str = None) -> int:
        ...
