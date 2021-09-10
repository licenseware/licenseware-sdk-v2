from typing import List
from licenseware.common.validators.file_validators import GeneralValidator
from licenseware.utils.file_utils import save_file
from licenseware.utils.logger import log



class FileContentValidator:
    
    def __init__(
        self,
        uploader_id:str,
        required_input_type:str = None,
        required_sheets:list = [],
        required_columns:list = [],
        text_contains_all:list = [],
        text_contains_any:list = [],
        min_rows_number:int = 0,
        header_starts_at:int = 0,
        buffer:int = 9000,
        **kwargs
    ):
        self.uploader_id = uploader_id
        self.required_input_type = required_input_type
        self.required_sheets = required_sheets
        self.required_columns = required_columns
        self.text_contains_all = text_contains_all
        self.text_contains_any = text_contains_any
        self.min_rows_number = min_rows_number
        self.header_starts_at = header_starts_at
        self.buffer = buffer
        self.kwargs = kwargs
    

    def get_file_objects_from_request(self, flask_request):
        
        file_objects = flask_request.files.getlist("files[]")
        
        bad_request = {
            "status": "fail", 
            "message": "File list is empty or files are not on 'files[]' key"
        }, 400
        
        if not isinstance(file_objects, list): return bad_request
        if file_objects == []: return bad_request
        
        return file_objects
    
    
    def get_only_valid_file_objects(self, file_objects:list) -> List[str]:
        
        filenames = [f.filename for f in file_objects] 
        filenames_validation_response = self.validate_filenames(filenames)
        
        valid_filenames = []
        for response in filenames_validation_response:
            if response['status'] == 'success':
                valid_filenames.append(response['filename'])
                
        validation_file_objects = []
        for file in file_objects:
            if file.filename in valid_filenames: 
                validation_file_objects.append(file)
            else:
                file.close()
                
        return validation_file_objects
        

    def validate_file_objects(self, file_objects:list, tenant_id:str) -> list:
        
        valid_file_objects = self.get_only_valid_file_objects(file_objects)
        
        validation_response = []
        for file in valid_file_objects:
            try:
            
                GeneralValidator(
                    input_object        = file,
                    required_input_type = self.required_input_type,
                    required_sheets     = self.required_sheets,
                    required_columns    = self.required_columns, 
                    text_contains_all   = self.text_contains_all,
                    text_contains_any   = self.text_contains_any,
                    min_rows_number     = self.min_rows_number,
                    header_starts_at    = self.header_starts_at,
                    buffer              = self.buffer
                )
                
                #Save validated file to disk
                filepath = save_file(file, tenant_id)
                
                validation_response.append({
                    'status': 'success',
                    'filename': file.filename, 
                    'filepath': filepath,
                    'message': self.filename_valid_message
                })
                
            except Exception as err:
                validation_response.append({
                    'status': 'fail',
                    'filename': file.filename, 
                    'filepath': 'File not saved',
                    'message': self.filename_invalid_message or str(err)
                })
                
        return validation_response

        
    def get_overall_status_and_message(self, validation_response:list):
    
        status  = 'success'
        message = 'Files are valid'
        for res in validation_response:
            if res['status'] == 'fail':        
                status  = 'fail'
                message = 'Not all files are valid'
                break
            
        return status, message
        
        
    def get_file_objects_response(self, flask_request):
        """
            receive flask_request 
            validate file names and file contents
            save to disk valid files
            create json response
        """
        
        tenant_id = flask_request.headers.get("Tenantid")
    
        file_objects = self.get_file_objects_from_request(flask_request)
        if not isinstance(file_objects, list): return file_objects
        validation_response = self.validate_file_objects(file_objects, tenant_id)
        status, message = self.get_overall_status_and_message(validation_response)
        
        return {
            'tenant_id': tenant_id, 
            'status': status, 
            'message': message,
            'validation': validation_response
        }, 200
            
            
        
            
            
        