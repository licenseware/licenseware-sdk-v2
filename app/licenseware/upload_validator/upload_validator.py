from typing import Any, Tuple
from .filename_validator import FileNameValidator
from .file_content_validator import FileContentValidator



class UploadValidator(FileNameValidator, FileContentValidator):
    
    """

    rv_tools_validator = UploadValidator(
        uploader_id = 'rv_tools',
        filename_contains = ['RV', 'Tools'],
        filename_endswith = ['.xls', '.xlsx'],
        ignore_filenames  = ['skip_this_file.csv'],
        required_input_type = "excel",
        min_rows_number = 1,
        required_sheets = ['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
        required_columns = [
            'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
            'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
            'Name', 'NumCpuThreads', 'NumCpuCores'
        ]
    )
        
        
    response, status_code = rv_tools_validator.get_filenames_response(flask_request)
    log.debug(response)
    {'status': 'success', 'message': 'Filenames are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'message': 'Filename is valid'}, {'status': 'fail', 'filename': 'randomfile.pdf', 'message': 'File must contain at least one of the following keywords: RV, Tools'}, {'status': 'ignored', 'filename': 'skip_this_file.csv', 'message': 'Filename is ignored'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}

    response, status_code = rv_tools_validator.get_file_objects_response(flask_request)
    log.debug(response)
    {'status': 'success', 'message': 'Files are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'message': 'Filename is valid'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}
    
    """
    
    def __init__(
        self,
        uploader_id:str,
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
        
        
    def get_filepaths_from_objects_response(self, file_objects_response):
        
        files_paths = [
            res['filepath'] 
            for res in file_objects_response['validation']
        ]
            
        return files_paths
    
    
    def calculate_quota(self, flask_request: Any, files: Any, uploader_id:str) -> Tuple[dict, int]:
        """
            receive flask_request and files objects from which we can calculate quota
            
            - get from flask_request the tenantid
            - calculate depending on uploader_id and files the quota remaining 
            - files will be either a list of filenames strings either a list of file objects (FileStorage objects)
        """
        #TODO
        # raise Exception("Please overwrite `calculate_quota` function")
        return {'status': 'success', 'message': 'Quota within limits'}, 200


