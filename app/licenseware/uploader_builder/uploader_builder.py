



from typing import Callable


class UploaderBuilder:
    
    def __init__(
        self, 
        id:str, 
        name:str, 
        description:str, 
        accepted_file_types:list, 
        validator: Callable,
        **kwargs
    ):
        self.id = id # validate id to be only lowercase with underscores
        self.name = name
        self.description = description
        self.accepted_file_types = accepted_file_types    
        self.validator = validator
    