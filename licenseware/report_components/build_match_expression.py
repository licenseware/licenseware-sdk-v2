from typing import List


def in_list_expression_builder(column, filter_value):
    return {"$expr": {"$in": [f"${column}", filter_value]}}


def equals_expression_builder(column, filter_value):
    return {column: filter_value}


def contains_expression_builder(column, filter_value):
    return {column: {"$regex": filter_value}}


def greater_than_expression_builder(column, filter_value):
    return {column: {"$gt": filter_value}}


def greater_or_equal_to_expression_builder(column, filter_value):
    return {column: {"$gte": filter_value}}


def less_than_expression_builder(column, filter_value):
    return {column: {"$lt": filter_value}}


def less_or_equal_to_expression_builder(column, filter_value):
    return {column: {"$lte": filter_value}}


condition_switcher = {
    "equals": equals_expression_builder,
    "contains": contains_expression_builder,
    "in_list": in_list_expression_builder,
    "greater_than": greater_than_expression_builder,
    "greater_or_equal_to": greater_or_equal_to_expression_builder,
    "less_than": less_than_expression_builder,
    "less_or_equal_to": less_or_equal_to_expression_builder,
}


def build_match_expression(filter_payload: List[dict]) -> dict:
    """

    Contructs the mongo $match expression from a given list of dicts

    Filter metadata example: [
        {
            "column": "name",
            "allowed_filters": ["equals", "contains", "in_list"],
            "visible_name": "Device Name",
            "column_type": "string" or "number" or TODO add more types here

        }
    ]

    Filter comming from frontend: [
        {
            column: "name",
            filter_type: "equals",
            filter_value: "the device name"
        }
    ]

    """

    parsed_filter = {}
    for filter_section in filter_payload:
        if not isinstance(filter_section, dict):
            continue
        if sorted(["column", "filter_type", "filter_value"]) != sorted(
            filter_section.keys()
        ):
            continue
        parsed_filter.update(
            condition_switcher[filter_section["filter_type"]](
                filter_section["column"], filter_section["filter_value"]
            )
        )

    return parsed_filter
