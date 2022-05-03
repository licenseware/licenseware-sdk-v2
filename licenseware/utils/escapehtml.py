import html
import json
from typing import Any


def escapehtml(data: Any):
    """
        Escape any html tags to prevent XSS attacks
    """

    if data is None: return
    
    strdata = html.escape(str(data), quote=False)
    
    if type(data) in [dict, list, tuple, set]:
        strdata = strdata.replace("'", '"')
        try:
            escaped_data = json.loads(strdata)
        except json.JSONDecodeError:
            return data
    else:
        escaped_data = type(data)(strdata)
    
    return escaped_data












