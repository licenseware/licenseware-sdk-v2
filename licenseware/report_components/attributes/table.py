import re
from typing import List


def attributes_table(props: List[str]):
    """

    From this input:
    props = ['number_of_databases', 'edition']

    The result will be a dictionary like bellow:
    {'columns': [
        {
            'name': 'Number of databases',
            'prop': 'number_of_databases',
            'type': 'string'
        },
        {
            'name': 'Edition',
            'prop': 'edition',
            'type': 'string'
        }
    ]}

    From this input:
    props = [('number_of_databases', 'number'), 'edition']


    The result will be a dictionary like bellow:

    {'columns': [
        {
            'name': 'Number of databases',
            'prop': 'number_of_databases',
            'type': 'number'
        },
        {
            'name': 'Edition',
            'prop': 'edition',
            'type': 'string'
        }
    ]}

    If given a tuple the second value from the tuple will be set as type for that column.
    By default typle will be string.

    """

    prop_columns = {"columns": []}

    for prop in props:

        name = prop[0] if isinstance(prop, tuple) else prop
        col_type = prop[1] if isinstance(prop, tuple) else "string"

        prop_columns["columns"].append(
            {
                "name": re.sub("_", " ", name).capitalize(),
                "prop": name,
                "type": col_type,
            }
        )

    return prop_columns
