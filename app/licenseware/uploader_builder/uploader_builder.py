from typing import Type
from app.licenseware.common.constants import envs, states
from app.licenseware.registry_service.register_uploader import register_uploader
from app.licenseware.utils.dramatiq_redis_broker import broker
from app.licenseware.utils.logger import log 



class UploaderBuilder:
    
    def __init__(
        self, 
        name:str, 
        description:str, 
        accepted_file_types:list, 
        validator_class: Type, 
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

        self.uploader_id = validator_class.uploader_id
        self.flags = flags
        self.status = status
        self.icon = icon
        
        # Paths for internal usage
        self.upload_path = upload_path or f"/{self.uploader_id}/files"
        self.upload_validation_path = upload_validation_path or f"/{self.uploader_id}/validation"
        self.quota_validation_path = quota_validation_path or f"/quota/{self.uploader_id}"
        self.status_check_path = status_check_path or f"/{self.uploader_id}/status"
        
        # Urls for registry service
        self.upload_url = envs.UPLOAD_URL + self.upload_path
        self.upload_validation_url = envs.UPLOAD_URL + self.upload_validation_path
        self.quota_validation_url = envs.UPLOAD_URL + self.quota_validation_path
        self.status_check_url = envs.UPLOAD_URL + self.status_check_path
        
        self.kwargs = kwargs
        
        self.uploader_vars = vars(self)
        
        
    def register_uploader(self):
        response, status_code = register_uploader(**self.uploader_vars)
        if status_code != 200:
            raise Exception("Uploader can't register to registry service")


    def validate_filenames(self, flask_request):
        
        response, status_code = self.validator_class.calculate_quota(flask_request)
        if response['status'] == 'fail': return response, status_code
        
        response, status_code = self.validator_class.get_filenames_response(flask_request)
        return response, status_code
    
        
    def upload_files(self, flask_request):
        
        quota_response, status_code = self.validator_class.calculate_quota(flask_request)
        if quota_response['status'] == 'fail': return quota_response, status_code
        
        response, status_code = self.validator_class.get_file_objects_response(flask_request)
        
        #TODO send event data to worker function
        event_data = {
            'tenant_id': flask_request.headers.get("TenantId"),
            'filepaths': self.validator_class.get_only_valid_filepaths_from_objects_response(response),
            'flask_request':  flask_request
        }
        
        (event_data)
        
        return response, status_code
    
    
    def init_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'TODO'}, 200
    
    def upload_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'TODO'}, 200
    
    def check_tenant_quota(self, tenant_id:str):
        #TODO
        return {'status': 'TODO'}, 200
        
        
        
        
        