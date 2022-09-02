import re
from typing import List, Tuple


def attributes_pie(label_value_key: List[Tuple]):
    """

    From this input:
    label_value_key = [("edition", "number_of_databases")]

    Will return this output:
    {'series': [
        {
            'label_description': 'Edition',
            'label_key': 'edition'
        },
        {
            'value_description': 'Number of databases',
            'value_key': 'number_of_databases'
        }
    ]}

    """

    props_series = {"series": []}

    for lv in label_value_key:

        props_series["series"].append(
            {
                "label_description": re.sub("_", " ", lv[0]).capitalize(),
                "label_key": lv[0],
            }
        )

        props_series["series"].append(
            {
                "value_description": re.sub("_", " ", lv[1]).capitalize(),
                "value_key": lv[1],
            }
        )

    return props_series
