import re



def table_props(machine_names:list) -> list:
    """
    
    :machine_names - list of machine_names: ['number_of_devices', 'number_of_databases'] 
    
    The result will be a dictionary like bellow:
    
    {
        'columns': [
            {
                'name': 'Number of Devices',
                'machine_name': 'number_of_devices'
            },
            {
                'name': 'Number of Databases',
                'machine_name': 'number_of_databases'
            },

        ]
    }
    
    """
    
    prop_columns = {'columns': []}
  
    for mn in machine_names:
        prop_columns['columns'].append({
            'name': re.sub('_', ' ', mn).capitalize(),
            'machine_name': mn
        })
        
    return prop_columns
        
            