from licenseware.uploader_validator import UploaderValidator



# If overwriting bellow mentioned methods is not necessary you can use `UploaderValidator` directly 
class {{ uploader_id.split('_') | map('title') | join('') }}UploaderValidator(UploaderValidator): 
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
{{ uploader_id }}_validator = {{ uploader_id.split('_') | map('title') | join('') }}UploaderValidator(
    filename_contains = ['RV', 'Tools'],
    filename_endswith = ['.xls', '.xlsx'],
    ignore_filenames  = ['skip_this_file.csv'],
    required_input_type = "excel",
    min_rows_number = 1,
    header_starts_at = 0,
    required_sheets  = ['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
    required_columns = [
        'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
        'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
        'Name', 'NumCpuThreads', 'NumCpuCores'
    ]
)

