from typing import List
from app.licenseware.common.validators.file_validators import GeneralValidator
from app.licenseware.utils.file_utils import save_file


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
        if not isinstance(file_objects, list) and file_objects:
            return {"status": "fail", "message": "key needs to be files[]"}
        
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

        
    def get_file_objects_response(self, flask_request):
        
        tenant_id = flask_request.headers.get("TenantId")
    
        file_objects = self.get_file_objects_from_request(flask_request)
        if not isinstance(file_objects, list): return file_objects
        validation_response = self.validate_file_objects(file_objects, tenant_id)
        
        response, status_code = self.calculate_quota(flask_request, file_objects, self.uploader_id)

        if response['status'] == 'fail':
            return response, status_code
        
        return {
            'status': 'success', 
            'message': 'Files are valid',
            'validation': validation_response,
            'quota': response
        }, 200
            
            
        