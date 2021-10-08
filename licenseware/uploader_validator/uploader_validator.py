import os
from typing import Tuple

from flask import Request

from licenseware.quota import Quota
from licenseware.utils.logger import log
from licenseware.common.constants import states
from marshmallow.fields import Boolean

from .filename_validator import FileNameValidator
from .file_content_validator import FileContentValidator







class UploaderValidator(FileNameValidator, FileContentValidator):
    
    """

    """
    
    def __init__(
        self,
        filename_contains:list = [],
        filename_endswith:list = [],
        ignore_filenames:list = [],
        required_input_type:str = None,
        required_sheets:list = [],
        required_columns:list = [],
        text_contains_all:list = [],
        text_contains_any:list = [],
        min_rows_number:int = 0,
        header_starts_at:int = 0,
        buffer:int = 9000,
        filename_valid_message = "Filename is valid",
        filename_invalid_message =  None,
        filename_ignored_message =  "Filename is ignored",
        _uploader_id:str = None,
        _quota_units:int = None, 
    ):
        self.quota_units = _quota_units
        self.uploader_id = _uploader_id
        self.filename_contains = filename_contains
        self.filename_endswith = filename_endswith
        self.ignore_filenames = ignore_filenames
        self.required_input_type = required_input_type
        self.required_sheets = required_sheets
        self.required_columns = required_columns
        self.text_contains_all = text_contains_all
        self.text_contains_any = text_contains_any
        self.min_rows_number = min_rows_number
        self.header_starts_at = header_starts_at
        self.buffer = buffer
        self.filename_valid_message = filename_valid_message
        self.filename_invalid_message = filename_invalid_message
        self.filename_ignored_message = filename_ignored_message
        self.validation_parameters = self.get_validation_parameters()
        super().__init__(**vars(self))
     
    
    def quota_within_limits(self, tenant_id:str, auth_token:str, units: int) -> Tuple[dict, int]:
        
        q = Quota(
            tenant_id=tenant_id, 
            auth_token=auth_token,
            uploader_id=self.uploader_id, 
            units=self.quota_units
        )
        
        _, status_code = q.check_quota(units)
        
        return _, status_code
    
    
    def update_quota(self, tenant_id:str, auth_token:str, units: int) -> Tuple[dict, int]:
        
        q = Quota(
            tenant_id=tenant_id, 
            auth_token=auth_token,
            uploader_id=self.uploader_id, 
            units=self.quota_units
        )
        
        response, status_code = q.update_quota(units)
        
        return response, status_code
        
        
    def calculate_quota(self, flask_request: Request, update_quota_units: bool = True) -> Tuple[dict, int]:
        
        if self.quota_units is None: 
            return {'status': states.SUCCESS, 'message': 'Quota is skipped'}, 200
        
        log.warning("Calculating quota based on length of files")
        
        tenant_id = flask_request.headers.get('Tenantid')
        auth_token = flask_request.headers.get('Authorization')
        file_objects = flask_request.files.getlist("files[]")
        
        current_units_to_process = len(file_objects)
        
        quota_check_status, quota_check_response = self.quota_within_limits(tenant_id, auth_token, current_units_to_process)


        if quota_check_status == 200 & update_quota_units: self.update_quota(tenant_id, auth_token, current_units_to_process)
            #return {'status': states.SUCCESS, 'message': 'Quota within limits'}, 200
        
        return quota_check_status, quota_check_response
    
        
    @classmethod
    def get_filepaths_from_objects_response(cls, file_objects_response):
        
        file_paths = [
            res['filepath'] 
            for res in file_objects_response['validation']
        ]
            
        return file_paths
    
    
    @classmethod
    def get_only_valid_filepaths_from_objects_response(cls, file_objects_response):
        
        file_paths = [
            res['filepath'] 
            for res in file_objects_response['validation']
            if res['filepath'] != 'File not saved' and os.path.exists(res['filepath'])
        ]
            
        return file_paths
  
    

    def get_validation_parameters(self):
        
        if not hasattr(self, 'vars'): return {}
        
        validators = vars(self)
        
        params_list = [
            'filename_contains',
            'filename_endswith',
            'ignore_filenames',
            'required_input_type',
            'required_sheets',
            'required_columns',
            'text_contains_all',
            'text_contains_any',
            'min_rows_number',
            'header_starts_at',
            'buffer',
            'filename_valid_message',
            'filename_invalid_message',
            'filename_ignored_message'                                        
        ]
        
        return {k:v for k,v in validators.items() if k in params_list}

        