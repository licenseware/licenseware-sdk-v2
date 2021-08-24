from typing import List
from app.licenseware.utils.logger import log



def in_list_expression_builder(field_name, filter_value):
    return {
        '$expr': {
            '$in': [f'${field_name}', filter_value]
        }
    }


def equals_expression_builder(field_name, filter_value):
    return {
        field_name: filter_value
    }


def contains_expression_builder(field_name, filter_value):
    return {
        field_name: {'$regex': filter_value}
    }


def greater_than_expression_builder(field_name, filter_value):
    return {
        field_name: {'$gt': filter_value}
    }


def greater_or_equal_to_expression_builder(field_name, filter_value):
    return {
        field_name: {'$gte': filter_value}
    }


def less_than_expression_builder(field_name, filter_value):
    return {
        field_name: {'$lt': filter_value}
    }


def less_or_equal_to_expression_builder(field_name, filter_value):
    return {
        field_name: {'$lte': filter_value}
    }



condition_switcher = {
    "equals": equals_expression_builder,
    "contains": contains_expression_builder,
    "in_list": in_list_expression_builder,
    "greater_than": greater_than_expression_builder,
    "greater_or_equal_to": greater_or_equal_to_expression_builder,
    "less_than": less_than_expression_builder,
    "less_or_equal_to": less_or_equal_to_expression_builder
}


def build_match_expression(filter_payload: List[dict]) -> dict:
    """
    
    Contructs the mongo $match expression from a given list of dicts
    
    Filter metadata example: [
        {
            field_name: "name", 
            allowed_filters: ["equals", "contains", "in_list"], 
            visible_name: "Device Name"
        }
    ]
    
    Filter comming from frontend: [
        {
            field_name: "name", 
            filter_type: "equals", 
            filter_value: "the device name"
        }
    ]
    
    """
    
    parsed_filter = {}
    for filter_section in filter_payload:
        parsed_filter.update(
            condition_switcher[filter_section["filter_type"]](
                filter_section["field_name"], filter_section["filter_value"]
            )
        )
        
    return {
        '$match': parsed_filter
    }

    