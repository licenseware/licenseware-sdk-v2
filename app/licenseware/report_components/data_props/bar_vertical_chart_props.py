import re


def bar_vertical_chart_props(xaxis_machine_name:str, yaxis_machine_name:str):
    """
    
    From this input:
    xaxis_machine_name="option_name", yaxis_machine_name="number_of_databases"
    
    Will return this output:
    {'series': [
        {'xaxis_name': 'Option name', 'xaxis_machine_name': 'option_name'},
        {'yaxis_name': 'Number of databases','yaxis_machine_name': 'number_of_databases'}
    ]}
    
    """
    
    props_series = {'series': [
        {
            'xaxis_name': re.sub('_', ' ', xaxis_machine_name).capitalize(),
            'xaxis_machine_name': xaxis_machine_name
        },
        {
            'yaxis_name': re.sub('_', ' ', yaxis_machine_name).capitalize(),
            'yaxis_machine_name': yaxis_machine_name
        },
    ]}
    
    return props_series

