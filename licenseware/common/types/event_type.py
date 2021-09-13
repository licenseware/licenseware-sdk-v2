from typing import NamedTuple



class Event(NamedTuple):
    tenant_id:str 
    uploader_id:str
    filepaths:list
    flask_request:dict
    validation_response:dict
    