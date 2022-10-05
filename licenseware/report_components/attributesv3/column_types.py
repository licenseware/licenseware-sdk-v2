from .base_enum import BaseEnum


class ColumnTypes(BaseEnum):
    STRING = "string"
    NUMBER = "number"
    DATE = "date"
    BOOL = "bool"
    JSON = "json"
    ENUM = "enum"
    ENTITY = "entity"
