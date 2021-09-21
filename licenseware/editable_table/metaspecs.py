


def metaspecs(
    editable:bool = False, 
    visible:bool = True,
    distinct_key:str = None, 
    foreign_key:str = None
):
   
    return {
        'editable': editable,
        'visible': visible,
        'distinct_key': distinct_key,
        'foreign_key': foreign_key
    }
    
    