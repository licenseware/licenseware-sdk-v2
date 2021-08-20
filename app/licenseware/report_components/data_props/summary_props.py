import re
from typing import List, Tuple


def summary_props(machine_names_icons:List[Tuple]) -> list:
    """
        From a list o tuples which contain machine name and icon name (use icons dataclass)
        machine_names_icons = [
            ("number_of_devices", "ServersIcon"), 
            ("number_of_databases", "DatabaseIconRounded")
        ]
        
        Will generate this output:
        
        {'series': [
        {'name': 'Number of devices',
           'machine_name': 'number_of_devices',
           'icon': 'ServersIcon'},
        {'name': 'Number of databases',
           'machine_name': 'number_of_databases',
           'icon': 'DatabaseIconRounded'}
        ]}
           
    """
    

    props_series = {'series': []}
    
    for mn_icon in machine_names_icons:
        props_series['series'].append({
            "name": re.sub('_', ' ', mn_icon[0]).capitalize(),
            "machine_name": mn_icon[0],
            "icon": mn_icon[1]
        })
        
    return props_series

