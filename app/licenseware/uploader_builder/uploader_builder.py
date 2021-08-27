from typing import Callable, Type
from app.licenseware.common.constants import envs, states
from app.licenseware.registry_service.register_uploader import register_uploader
from app.licenseware.utils.dramatiq_redis_broker import broker
from app.licenseware.utils.logger import log, log_dict
from app.licenseware.quota import Quota



class UploaderBuilder:
    
    """
    
    name:str - name of the uploader
    uploader_id:str - uploader_id, this should be unique for each app declared
    description:str - description of this uploader, what type of files it accepts 
    accepted_file_types:list - accepted file formats .xlsx, .pdf etc 
    validator_class: Type -  this is a UploaderValidator class instance
    worker_function: Callable - this is responsible for processing the received files (receives a dict with tenant_id and absolute paths to files)
    quota_units:int - number of units allowed to be processed for free each month
    flags:list = [] - stage of the development see constants.flags dataclass to see/add values
    status:str = states.IDLE - state of the worker_function it it's processing or not the files
    icon:str = "default.png" - icon for this uploader see constants.icons dataclass to see/add more
    upload_path:str = None - url path/route where files will be updated
    upload_validation_path:str = None - url path/route where filenames will be validated
    quota_validation_path:str = None - url path/route where quota for this uploader_id is checked
    status_check_path:str = None - url path/route where gives back the status of the worker function
    
    """
    
    def __init__(
        self, 
        name:str, 
        uploader_id:str,
        description:str, 
        accepted_file_types:list, 
        validator_class: Type, 
        worker_function: Callable,
        quota_units:int,
        flags:list = [],
        status:str = states.IDLE,
        icon:str = "default.png",
        upload_path:str = None,
        upload_validation_path:str = None,
        quota_validation_path:str = None,
        status_check_path:str = None,
        **kwargs
    ):
        
        if envs.ENVIRONMENT == 'local': 
            uploader_id = envs.PERSONAL_PREFIX + uploader_id

        #Passing variables to validator class
        validator_class.uploader_id = uploader_id
        validator_class.quota_units = quota_units
        
        self.uploader_id = uploader_id
        self.quota_units = quota_units
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
                'uploader_id': self.uploader_id,
                'headers':  dict(flask_request.headers) if flask_request.headers else {},
                'json':  dict(flask_request.json) if flask_request.json else {},
            }
            
            log_dict(event_data)
            self.worker.send(event_data)
            
            
        return response, status_code
    
    
    def init_tenant_quota(self, tenant_id:str):
        
        # Used in app_activation_path
        
        q = Quota(
            tenant_id=tenant_id, 
            uploader_id=self.uploader_id, 
            units=self.quota_units
        )
        
        response, status_code = q.init_quota()
        
        return response, status_code
    
    
    def check_tenant_quota(self, tenant_id:str):
        
        # Used for uploader_id/quota route
        
        q = Quota(
            tenant_id=tenant_id, 
            uploader_id=self.uploader_id, 
            units=self.quota_units
        )
        
        response, status_code = q.check_quota()
        
        return response, status_code
    
        
        
        