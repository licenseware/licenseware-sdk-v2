import re


def bar_vertical_chart_props(xaxis_slug_name:str, yaxis_slug_name:str):
    """
    
    From this input:
    xaxis_slug_name="option_name", yaxis_slug_name="number_of_databases"
    
    Will return this output:
    {'series': [
        {'xaxis_name': 'Option name', 'xaxis_slug_name': 'option_name'},
        {'yaxis_name': 'Number of databases','yaxis_slug_name': 'number_of_databases'}
    ]}
    
    """
    
    props_series = {'series': [
        {
            'xaxis_name': re.sub('_', ' ', xaxis_slug_name).capitalize(),
            'xaxis_slug_name': xaxis_slug_name
        },
        {
            'yaxis_name': re.sub('_', ' ', yaxis_slug_name).capitalize(),
            'yaxis_slug_name': yaxis_slug_name
        },
    ]}
    
    return props_series

