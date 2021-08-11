from typing import Callable
from app.licenseware.common.constants import states



# upload_url="/rvtools/files",
# upload_validation_url='/rvtools/validation',
# quota_validation_url='/quota/rvtools',
# status_check_url='/rvtools/status',
# history_url='/rvtools/history',


class UploaderBuilder:
    
    def __init__(
        self, 
        name:str, 
        description:str, 
        accepted_file_types:list, 
        validator: Callable, #TODO maybe a class with more options?
        app_id:str = None, 
        uploader_id:str = None,
        flags:list = None,
        status:str = states.IDLE,
        upload_url:str = None,
        upload_validation_url:str = None,
        quota_validation_url:str = None,
        status_check_url:str = None,
        **kwargs
    ):
        self.name = name
        self.description = description
        self.accepted_file_types = accepted_file_types
        self.validator = validator
        self.app_id = app_id or "" #TODO
        self.uploader_id = uploader_id or validator.__name__
        self.flags = flags
        self.status = status
        self.upload_url = upload_url
        self.upload_validation_url = upload_validation_url
        self.quota_validation_url = quota_validation_url
        self.status_check_url = status_check_url
        self.kwargs = kwargs
        
        