from licenseware.uploader_validator import UploaderValidator



# If overwriting bellow mentioned methods is not necessary you can use `UploaderValidator` directly 
class RvToolsUploaderValidator(UploaderValidator): 
    ...
    
    # def calculate_quota(self, flask_request) -> Tuple[dict, int]:
    # responsible for calculating quota based on tenant_id and returning a json response, status code 
    # ...
    
    # def get_filenames_response(self, flask_request): 
    # responsible for validating filenames and returning a json response, status code
    # ...
    
    # def get_file_objects_response(self, flask_request): 
    #   responsible for validating filenames, their contents and returning a json response, status code
    # ...
    
    
    
# Fill parameters as per uploader needs 
rv_tools_validator = RvToolsUploaderValidator(
    filename_contains = [],
    filename_endswith = [],
    ignore_filenames  = [],
    required_input_type = None,
    min_rows_number = 1,
    header_starts_at = 0,
    required_sheets = [],
    required_columns = []
)
