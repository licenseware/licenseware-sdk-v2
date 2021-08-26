from typing import Callable, Type
from app.licenseware.common.constants import envs, states
from app.licenseware.registry_service.register_uploader import register_uploader
from app.licenseware.utils.dramatiq_redis_broker import broker
from app.licenseware.utils.logger import log, log_dict
from app.licenseware.quota import Quota



class UploaderBuilder:
    
    def __init__(
        self, 
        name:str, 
        uploader_id:str,
        description:str, 
        accepted_file_types:list, 
        validator_class: Type, 
        worker_function: Callable,
        flags:list = [],
        status:str = states.IDLE,
        icon:str = "default.png",
        upload_path:str = None,
        upload_validation_path:str = None,
        quota_validation_path:str = None,
        status_check_path:str = None,
        **kwargs
    ):
        
        validator_class.uploader_id = uploader_id
        
        self.uploader_id = uploader_id
        self.name = name
        self.description = description
        self.validator_class = validator_class
        self.app_id = envs.APP_ID
        self.worker = broker.actor(worker_function, max_retries=3, actor_name=self.uploader_id, queue_name=envs.APP_ID)
        self.accepted_file_types = accepted_file_types
        self.flags = flags
        self.status = status
        self.icon = icon
        
        # Paths for internal usage
        self.upload_path = upload_path or f"/{self.uploader_id}/files"
        self.upload_validation_path = upload_validation_path or f"/{self.uploader_id}/validation"
        self.quota_validation_path = quota_validation_path or f"/{self.uploader_id}/quota"
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
        return response, status_code


    def validate_filenames(self, flask_request):
        
        quota_response, quota_status_code = self.validator_class.calculate_quota(flask_request)
        if quota_status_code != 200: return quota_response, quota_status_code
        
        response, status_code = self.validator_class.get_filenames_response(flask_request)
        return response, status_code
    
        
    def upload_files(self, flask_request):
        
        quota_response, quota_status_code = self.validator_class.calculate_quota(flask_request)
        if quota_status_code != 200: return quota_response, quota_status_code
        
        
        response, status_code = self.validator_class.get_file_objects_response(flask_request)
        
        if status_code == 200:
            
            event_data = {
                'tenant_id': flask_request.headers.get("Tenantid"),
                'filepaths': self.validator_class.get_only_valid_filepaths_from_objects_response(response),
                'headers':  dict(flask_request.headers) if flask_request.headers else {},
                'json':  dict(flask_request.json) if flask_request.json else {},
            }
            
            log_dict(event_data)
            self.worker.send(event_data)
            
            
        return response, status_code
    
    
    def init_tenant_quota(self, tenant_id:str):
        return Quota(tenant_id=tenant_id, uploader_id=self.uploader_id).init_quota()
    
    # def update_tenant_quota(self, tenant_id:str):
    #     return Quota(tenant_id=tenant_id, uploader_id=self.uploader_id).init_quota()
    
    def check_tenant_quota(self, tenant_id:str):
        return Quota(tenant_id=tenant_id, uploader_id=self.uploader_id).check_quota()
        
        
        
        