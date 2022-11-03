from .base_enum import BaseEnum


class AllowedFilters(BaseEnum):
    EQUALS = "equals"
    CONTAINS = "contains"
    IN_LIST = "in_list"
    GREATER_THAN = "greater_than"
    GREATER_OR_EQUAL_TO = "greater_or_equal_to"
    LESS_THAN = "less_than"
    LESS_OR_EQUAL_TO = "less_or_equal_to"
