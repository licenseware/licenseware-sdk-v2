import re
from typing import List, Tuple


def attributes_summary(value_key_and_icon: List[Tuple]) -> list:
    """
    From a list o tuples which contain `value_key` and `icon` name (use icons dataclass)

    value_key_and_icon = [
        ("number_of_devices", "ServersIcon"),
        ("number_of_databases", "DatabaseIconRounded")
    ]

    Will generate this output:

    {'series': [
        {
            'value_description': 'Number of devices',
            'value_key': 'number_of_devices',
            'icon': 'ServersIcon'
        },
        {
           'value_description': 'Number of databases',
           'value_key': 'number_of_databases',
           'icon': 'DatabaseIconRounded'
        }
    ]}

    """

    props_series = {"series": []}

    for vk_icon in value_key_and_icon:
        props_series["series"].append(
            {
                "value_description": re.sub("_", " ", vk_icon[0]).capitalize(),
                "value_key": vk_icon[0],
                "icon": vk_icon[1],
            }
        )

    return props_series
