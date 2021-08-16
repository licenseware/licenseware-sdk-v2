import os
from typing import Any, List
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


# END MOCK CLASS



def calculate_quota(files: Any) -> dict:
   #TODO add quota validation
   # files will be either a list of filenames strings either a list of file objects (FileStorage objects)
   return {'status': 'success', 'message': 'Quota within limits'}



class FileNameValidator:
    
    uploader_id = None
    ignore_filenames = []
    filename_contains = []
    filename_endswith = []
    filename_valid_message = "Filename is valid"
    filename_invalid_message =  None
    filename_ignored_message =  "Filename is ignored"

    def get_filenames_from_request(self, flask_request):
    
        filenames = flask_request.json

        if not isinstance(filenames, list):
            return {'status': 'fail', 'message': 'Filenames sent for validation must be in a list of strings format'}
            
        if len(filenames) == 0:
            return {'status': 'fail', 'message': 'Filenames sent for validation must be in a list of strings format'}

        return filenames
    
    
    def validate_filenames(self, filenames:list) -> list:

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
    

    @classmethod
    def get_filenames_response(cls, flask_request):
    
        filenames = cls().get_filenames_from_request(flask_request)
        if not isinstance(filenames, list): return filenames
        validation_response = cls().validate_filenames(filenames)
        
        
        quota_response = calculate_quota(filenames)
        
        status  = 'success'
        message = 'Filenames are valid.'
        
        if quota_response['status'] == 'fail':
            status  = quota_response['status']
            message = quota_response['message']
        
        return {
            'status': status, 
            'message': message,
            'validation': validation_response,
            'quota': quota_response
        }, 200



class FileContentValidator:
    
    required_input_type = None
    required_sheets = []
    required_columns = []
    text_contains_all = []
    text_contains_any = []
    min_rows_number = 0
    header_starts_at = 0
    buffer = 9000
    
    
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
        

    def validate_file_objects(self, file_objects:list) -> list:
        
        valid_file_objects = self.get_only_valid_file_objects(file_objects)
        
        for file in valid_file_objects:
            try:
                
                GeneralValidator(
                    input_object=file,
                    required_input_type = self.required_input_type,
                    required_sheets = self.required_sheets,
                    required_columns = self.required_columns, 
                    text_contains_all = self.text_contains_all,
                    text_contains_any = self.text_contains_any,
                    min_rows_number = self.min_rows_number,
                    header_starts_at = self.header_starts_at,
                    buffer = self.buffer
                )
                
                
                
            except Exception as err:
                print(err)
        
         
    @classmethod
    def get_file_objects_response(cls, flask_request):
    
        file_objects = cls().get_file_objects_from_request(flask_request)
        if not isinstance(file_objects, list): return file_objects
        validation_response = cls().validate_file_objects(file_objects)
        
        
        quota_response = calculate_quota(file_objects)
        
        status  = 'success'
        message = 'Files are valid.'
        
        if quota_response['status'] == 'fail':
            status  = quota_response['status']
            message = quota_response['message']
        
        return {
            'status': status, 
            'message': message,
            'validation': validation_response,
            'quota': quota_response
        }, 200
            
            
        
    


class FileValidator(FileNameValidator, FileContentValidator): ...



class ValidateRVTools(FileValidator):
    
    filename_contains = ['RV', 'Tools']
    filename_endswith = ['.xls', '.xlsx']
    ignore_filenames  = ['skip_this_file.csv']
    
    
    
log.debug(flask_request)


response, status_code = ValidateRVTools.get_filenames_response(flask_request)
log.debug(response)


response, status_code = ValidateRVTools.get_file_objects_response(flask_request)
log.debug(response)





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



def _filenames_response(self, request_obj, filename_ok_msg='Filename is valid.', filename_nok_msg='Filename is not valid.'):

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
        'message': 'Filenames are valid.',
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
