from dataclasses import dataclass


@dataclass(frozen=True)
class filters:
    EQUALS:str = "equals"
    CONTAINS:str = "contains"
    IN_LIST:str = "in_list"
    GREATER_THAN:str = "greater_than"
    GREATER_THAN_OR_EQUAL_TO:str = "greater_or_equal_to"
    LESS_THAN:str = "less_than"
    LESS_THAN_OR_EQUAL_TO:str = "less_or_equal_to"
    