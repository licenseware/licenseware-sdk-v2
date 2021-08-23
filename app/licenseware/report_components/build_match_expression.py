
def in_list_expression_builder(column, filter_value):
    return {
        '$expr': {
            '$in': [f'${column}', filter_value]
        }
    }


def equals_expression_builder(column, filter_value):
    return {
        column: filter_value
    }


def contains_expression_builder(column, filter_value):
    return {
        column: {'$regex': filter_value}
    }


def greater_than_expression_builder(column, filter_value):
    return {
        column: {'$gt': filter_value}
    }


def greater_or_equal_to_expression_builder(column, filter_value):
    return {
        column: {'$gte': filter_value}
    }


def less_than_expression_builder(column, filter_value):
    return {
        column: {'$lt': filter_value}
    }


def less_or_equal_to_expression_builder(column, filter_value):
    return {
        column: {'$lte': filter_value}
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


def build_match_expression(filter_payload):
    
    parsed_filter = {}
    for filter_section in filter_payload:
        parsed_filter.update(
            condition_switcher[filter_section["filter_type"]](
                filter_section["column"], filter_section["filter_value"]
            )
        )
    return {
        '$match': parsed_filter
    }

    