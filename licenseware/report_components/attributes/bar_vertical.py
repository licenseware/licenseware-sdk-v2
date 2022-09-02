import re
from typing import List, Tuple


def attributes_bar_vertical(xy_axis_key: List[Tuple]):
    """

    From this input:
    xy_axis_key = [("database", "oracle_processors_required")]

    Will return this output:
    {'series': [
        {
            'xaxis_description': 'Database',
            'xaxis_key': 'database'
        },
        {
             'yaxis_description': 'Oracle processors required',
             'yaxis_key': 'oracle_processors_required'
        }
    ]}

    """

    props_series = {"series": []}

    for xy in xy_axis_key:

        props_series["series"].append(
            {
                "xaxis_description": re.sub("_", " ", xy[0]).capitalize(),
                "xaxis_key": xy[0],
            }
        )

        props_series["series"].append(
            {
                "yaxis_description": re.sub("_", " ", xy[1]).capitalize(),
                "yaxis_key": xy[1],
            }
        )

    return props_series
