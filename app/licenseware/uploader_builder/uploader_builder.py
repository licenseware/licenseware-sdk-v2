from app.licenseware.registry_service.register_uploader import register_uploader
from typing import Callable
from app.licenseware.common.constants import envs, states
 

class UploaderBuilder:
    
    def __init__(
        self, 
        name:str, 
        description:str, 
        accepted_file_types:list, 
        validator: Callable, #TODO maybe a class with more options?
        uploader_id:str = None,
        flags:list = [],
        status:str = states.IDLE,
        icon:str = "default.png",
        upload_path:str = None,
        upload_validation_path:str = None,
        quota_validation_path:str = None,
        status_check_path:str = None,
        **kwargs
    ):
        self.name = name
        self.description = description
        self.accepted_file_types = accepted_file_types
        self.validator = validator
        self.app_id = envs.APP_ID
        
        if not uploader_id:
            
            if not validator.__name__.startswith('validate_'):
                raise ValueError("All validator functions must start with 'validate_' prefix and must be followed by the uploader_id (ex: validate_rv_tools)")
            
            uploader_id = validator.__name__.replace('validate_', '')
        
        self.uploader_id = uploader_id
        self.flags = flags
        self.status = status
        self.icon = icon
        self.upload_path = upload_path or f"/{uploader_id}/files"
        self.upload_validation_path = upload_validation_path or f"/{uploader_id}/validation"
        self.quota_validation_path = quota_validation_path or f"/quota/{uploader_id}"
        self.status_check_path = status_check_path or f"/{uploader_id}/status"
        
        self.upload_url = envs.UPLOAD_URL + self.upload_path
        self.upload_validation_url = envs.UPLOAD_URL + self.upload_validation_path
        self.quota_validation_url = envs.UPLOAD_URL + self.quota_validation_path
        self.status_check_url = envs.UPLOAD_URL + self.status_check_path
        self.kwargs = kwargs
        
        self.uploader_vars = vars(self)
        
        
        
    def register_uploader(self):
        register_uploader(**self.uploader_vars)

        
        