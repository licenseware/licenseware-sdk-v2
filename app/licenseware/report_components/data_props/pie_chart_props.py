import re


def pie_chart_props(machine_names:list):
    """
    
    From this input:
    machine_names = ["device_type", "number_of_devices"]
    
    Will return this output:
    {'series': [
        {'name': 'Device type', 'machine_name': 'device_type'},
        {'name': 'Number of devices', 'machine_name': 'number_of_devices'}
    ]}
    
    """
    
    props_series = {'series': []}
    
    for mn in machine_names:
        props_series['series'].append({
            'name': re.sub('_', ' ', mn).capitalize(),
            'machine_name': mn
        })
        
    return props_series

