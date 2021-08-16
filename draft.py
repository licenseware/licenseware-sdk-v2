import os
from typing import Any, List, Tuple
from app.licenseware.utils.logger import log
from app.licenseware.common.validators.file_validators import (
    GeneralValidator, 
    validate_filename
)


# MOCK CLASS

from werkzeug.datastructures import FileStorage


files_path = '/home/acmt/Documents/files_test/test_validators_files'
mock_filenames = ['rvtools.xlsx', "rv_tools.xlsx", 'randomfile.pdf', 'skip_this_file.csv'] 


class flask_request:
    
    json = mock_filenames
    
    class files:
        
        @classmethod
        def getlist(cls, key):
            
            if key != "files[]":
                raise Exception("Key 'files[]' doesn't exist")
            
            mock_binary_files = []
            for fname in mock_filenames:
                
                mock_file = FileStorage(
                    stream = open(os.path.join(files_path, fname), 'rb'),
                    filename = fname,
                    content_type = "application/*",
                )
                
                mock_binary_files.append(mock_file)

            return mock_binary_files
        
        
    class headers:
        
        @classmethod
        def get(cls, tenant_id):
            return "an uuid4 tenant id"
            



def save_file(file, tenant_id):
    #TODO
    return True

# END MOCK CLASS




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
                
                #TODO save files to disk
                save_file(file, tenant_id)
                
                validation_response.append({
                    'status': 'success',
                    'filename': file.filename, 
                    'message': self.filename_valid_message
                })
                
            except Exception as err:
                validation_response.append({
                    'status': 'fail',
                    'filename': file.filename, 
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
            
            
        

class UploadValidator(FileNameValidator, FileContentValidator):
    
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

response, status_code = rv_tools_validator.get_file_objects_response(flask_request)
log.debug(response)









    
    # uploader_id = None
    
    # # Same parameters as validate_filename
    # filename_contains = []
    # filename_endswith = []
    # ignore_filenames = []
    
    # # Same parameters as in GeneralValidator
    # required_input_type = None
    # required_sheets = []
    # required_columns = []
    # text_contains_all = []
    # text_contains_any = []
    # min_rows_number = 0
    # header_starts_at = 0
    # buffer = 9000

    # # Default messages
    # filename_valid_message = "Filename is valid"
    # filename_invalid_message =  None
    # filename_ignored_message =  "Filename is ignored"
    

    # def calculate_quota(self, flask_request: Any, files: Any, uploader_id:str) -> Tuple[dict, int]:
    #     """
    #         receive flask_request and files objects from which we can calculate quota
            
    #         - get from flask_request the tenantid
    #         - calculate depending on uploader_id and files the quota remaining 
    #         - files will be either a list of filenames strings either a list of file objects (FileStorage objects)
    #     """
    #     #TODO
    #     # raise Exception("Please overwrite `calculate_quota` function")
    #     return {'status': 'success', 'message': 'Quota within limits'}, 200




# class ValidateRVTools(UploadValidator):
    
#     uploader_id = 'rv_tools'
#     filename_contains = ['RV', 'Tools']
#     filename_endswith = ['.xls', '.xlsx']
#     ignore_filenames  = ['skip_this_file.csv']
#     required_input_type = "excel"
#     min_rows_number = 1
#     required_sheets = ['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster']
#     required_columns = [
#         'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
#         'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
#         'Name', 'NumCpuThreads', 'NumCpuCores'
#     ]
    
# response, status_code = ValidateRVTools.get_filenames_response(flask_request)
# log.debug(response)
# {'status': 'success', 'message': 'Filenames are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'message': 'Filename is valid'}, {'status': 'fail', 'filename': 'randomfile.pdf', 'message': 'File must contain at least one of the following keywords: RV, Tools'}, {'status': 'ignored', 'filename': 'skip_this_file.csv', 'message': 'Filename is ignored'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}



# response, status_code = ValidateRVTools.get_file_objects_response(flask_request)
# log.debug(response)
# {'status': 'success', 'message': 'Files are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'message': 'Filename is valid'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}







"""

# OLD

def _upload_response(self, request_obj, event_type):

    file_objects = request_obj.files.getlist("files[]")
    if not isinstance(file_objects, list) and file_objects:
        return {"status": "fail", "message": "key needs to be files[]"}, 400

    saved_files, validation = [], []
    for file in file_objects:
        res = self.validation_function(file, reason=True)
        if res['status'] == "success":
            filename = save_file(file, request_obj.headers.get("TenantId"))
            saved_files.append(filename)
        else:
            filename = file.filename

        validation.append({
            "filename": filename, "status": res['status'], "message": res['message']
        })


    if not saved_files:
        return {
            "status": "fail", "message": "no valid files provided", "validation": validation
        }, 400



    event = {
        "tenant_id": request_obj.headers.get("TenantId"),
        "files": ",".join(saved_files),
        "event_type": event_type
    }

    validate_event(event)
    broker.actors[event_type].send(event)

    # DramatiqEvent.send(event)
    # RedisService.send_stream_event({
    #     "tenant_id": request_obj.headers.get("TenantId"),
    #     "files": ",".join(saved_files),
    #     "event_type": event_type
    # })

    return {"status": "success", "message": "files uploaded successfuly", 
        "units": len(saved_files), 
        "validation": validation
    }, 200



def _filenames_response(self, request_obj, filename_ok_msg='Filename is valid', filename_nok_msg='Filename is not valid'):

    filenames = request_obj.json

    if not isinstance(filenames, list) and filenames:
        return {'status': 'fail', 'message': 'Must be a list of filenames.'}, 400

    validation, accepted_files = [], []
    for filename in filenames:
        status, message = 'fail', filename_nok_msg
        if self.validation_function(filename):
            accepted_files.append(filename)
            status, message = 'success', filename_ok_msg

        validation.append({
            "filename": filename, "status": status, "message": message
        })

    if not accepted_files:
        return {
            'status': 'fail', 
            'message': filename_nok_msg,
            'validation': validation,
            'units': 0
        }, 400

    return {
        'status': 'success', 
        'message': 'Filenames are valid',
        'validation': validation,
        'units': len(accepted_files)
    }, 200




def valid_rv_tools_file(file, reason=False):
    
    valid_fname, valid_contents = None, None
    
    if isinstance(file, str):
        valid_fname = validate_filename(file, ['RV', 'Tools'], ['.xls', '.xlsx'])
        valid_contents = True

    if "stream" in str(dir(file)):
        valid_fname = validate_filename(file.filename, ['RV', 'Tools'], ['.xls', '.xlsx'])
        if valid_fname:
            valid_contents = GeneralValidator(
                input_object=file,
                required_input_type="excel",
                min_rows_number=1,
                required_sheets=['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
                required_columns=[
                    'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
                    'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
                    'Name', 'NumCpuThreads', 'NumCpuCores'
                ]).validate(reason)

    filename_nok_msg = 'Files must be of type ".xls" or ".xlsx" and contain "RV" and/or "Tools" in filename.'
    return reason_response(reason, valid_fname, valid_contents, filename_nok_msg)


"""
