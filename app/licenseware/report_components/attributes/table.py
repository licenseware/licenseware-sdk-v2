import re
from typing import List



def attributes_table(props:List[str]):
    """

    From this input: 
    props = ['number_of_databases', 'edition'] 
    
    The result will be a dictionary like bellow:
    {'columns': [
        {
            'name': 'Number of databases', 
            'prop': 'number_of_databases'
        },
        {
            'name': 'Edition', 
            'prop': 'edition'
        }
    ]}
    
    """
    
    prop_columns = {'columns': []}
  
    for prop in props:
        prop_columns['columns'].append({
            'name': re.sub('_', ' ', prop).capitalize(),
            'prop': prop
        })
        
    return prop_columns
        
            