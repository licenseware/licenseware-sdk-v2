import os
from typing import Tuple
from .filename_validator import FileNameValidator
from .file_content_validator import FileContentValidator

from app.licenseware.utils.logger import log



class UploaderValidator(FileNameValidator, FileContentValidator):
    
    """

    """
    
    def __init__(
        self,
        uploader_id:str = None,
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
        filename_ignored_message =  "Filename is ignored"
    ):
        
        self.uploader_id = uploader_id
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
        
        super().__init__(**vars(self))
     
    
    def calculate_quota(self, flask_request) -> Tuple[dict, int]:
        """
            receive flask_request, extract tenantid and files, calculate quota
            - quota will be different for each uploader_id
        """
        raise NotImplementedError("Overwrite `calculate_quota` func")
    
        
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
    

