from typing import Type
from app.licenseware.common.constants import envs, states
from app.licenseware.registry_service.register_uploader import register_uploader
 


class UploaderBuilder:
    
    def __init__(
        self, 
        name:str, 
        description:str, 
        accepted_file_types:list, 
        validator_class: Type, 
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
        self.validator_class = validator_class
        self.app_id = envs.APP_ID
        
        if not uploader_id:
            
            if not validator_class.__name__.startswith('validate_'):
                raise ValueError("All validator classes must start with 'Validate' prefix \
                                 and must be followed by the 'uploader_id' (ex: ValidateRVTools)"
                            )
            
            uploader_id = validator_class.__name__.replace('Validate', '').lower()
        
        self.uploader_id = uploader_id
        self.flags = flags
        self.status = status
        self.icon = icon
        
        # Paths for internal usage
        self.upload_path = upload_path or f"/{uploader_id}/files"
        self.upload_validation_path = upload_validation_path or f"/{uploader_id}/validation"
        self.quota_validation_path = quota_validation_path or f"/quota/{uploader_id}"
        self.status_check_path = status_check_path or f"/{uploader_id}/status"
        
        # Urls for registry service
        self.upload_url = envs.UPLOAD_URL + self.upload_path
        self.upload_validation_url = envs.UPLOAD_URL + self.upload_validation_path
        self.quota_validation_url = envs.UPLOAD_URL + self.quota_validation_path
        self.status_check_url = envs.UPLOAD_URL + self.status_check_path
        
        self.kwargs = kwargs
        
        self.uploader_vars = vars(self)
        
        
        
    def register_uploader(self):
        return register_uploader(**self.uploader_vars)

    def init_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'success'}, 200
    
    def upload_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'success'}, 200
    
    def check_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'success'}, 200
        
        
    # def validate_filenames(self, flask_request):
    #     #TODO
    #     return {'status': 'success'}, 200
        
    # def upload_files(self, flask_request):
    #     #TODO
    #     return {'status': 'success'}, 200
        
        
        