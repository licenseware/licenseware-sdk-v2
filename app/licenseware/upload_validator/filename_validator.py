from typing import List
from app.licenseware.common.validators.file_validators import validate_filename


class FileNameValidator:
    
    """
        This class is reponsible for validating filenames
    """
    
    def __init__(
        self,
        uploader_id:str,
        ignore_filenames:list = [],
        filename_contains:list = [],
        filename_endswith:list = [],
        filename_valid_message = "Filename is valid",
        filename_invalid_message =  None,
        filename_ignored_message =  "Filename is ignored",
        **kwargs
    ):
        self.uploader_id = uploader_id
        self.ignore_filenames = ignore_filenames
        self.filename_contains = filename_contains
        self.filename_endswith = filename_endswith
        self.filename_valid_message = filename_valid_message
        self.filename_invalid_message = filename_invalid_message
        self.filename_ignored_message = filename_ignored_message
        #prevents overflow of params allows extending with non-default parameters
        self.kwargs = kwargs
        
        
    def get_filenames_from_request(self, flask_request):
        """
            validate request received
            filename validation request should be a list of filenames
        """
    
        filenames = flask_request.json

        if not isinstance(filenames, list):
            return {'status': 'fail', 'message': 'Filenames sent for validation must be in a list of strings format'}
            
        if len(filenames) == 0:
            return {'status': 'fail', 'message': 'Filenames sent for validation must be in a list of strings format'}

        return filenames
    
    
    def validate_filenames(self, filenames:List[str]) -> List[dict]:
        """
            receive a list of filenames and validate them based on 
            `filename_contains` and `filename_endswith` input parameters
            return a list of dicts with validation status, filename and message
            
            it's recomented to leave `filename_invalid_message` paramters as is 
            because if None will provide the reason why filename validation failed
        """

        validation_response = []
        for filename in filenames:
            
            if filename in self.ignore_filenames:
                
                validation_response.append({
                    'status': 'ignored',
                    'filename': filename, 
                    'message': self.filename_ignored_message
                })
                
                continue
            
            try:
                validate_filename(
                    filename, 
                    contains=self.filename_contains, 
                    endswith=self.filename_endswith
                )
                validation_response.append({
                    'status': 'success',
                    'filename': filename, 
                    'message': self.filename_valid_message
                })
            except Exception as err:
                validation_response.append({
                    'status': 'fail',
                    'filename': filename, 
                    'message': self.filename_invalid_message or str(err)
                })

        return validation_response
    

    def get_filenames_response(self, flask_request):
        """
            receive flask_request request start validation process,
            calculate quota and create the validation response 
        """
    
        filenames = self.get_filenames_from_request(flask_request)
        if not isinstance(filenames, list): return filenames
        validation_response = self.validate_filenames(filenames)
    
        response, status_code = self.calculate_quota(flask_request, filenames, self.uploader_id)
        
        if response['status'] == 'fail':
            return response, status_code
        
        return {
            'status': 'success', 
            'message': 'Filenames are valid',
            'validation': validation_response,
            'quota': response
        }, 200
