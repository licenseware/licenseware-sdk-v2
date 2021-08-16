import unittest

from app.licenseware.upload_validator import UploadValidator


# Mock objects
import os, io
from werkzeug.datastructures import FileStorage


files_path = '/home/acmt/Documents/files_test/test_validators_files'
mock_filenames = ['rvtools.xlsx', "rv_tools.xlsx", 'randomfile.pdf', 'skip_this_file.csv'] 

# Simulating a flask request object
class flask_request:
    
    json = mock_filenames
    
    class files:
        
        @classmethod
        def getlist(cls, key):
            
            if key != "files[]":
                raise Exception("Key 'files[]' doesn't exist")
            
            mock_binary_files = []
            for fname in mock_filenames:
                
                
                with open(os.path.join(files_path, fname), 'rb') as f:
                    file_binary = io.BytesIO(f.read())
                
                mock_file = FileStorage(
                    stream = file_binary,
                    filename = fname,
                    content_type = "application/*",
                )
                
                mock_binary_files.append(mock_file)

            return mock_binary_files
        
        
    class headers:
        
        @classmethod
        def get(cls, tenant_id):
            return '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'
            
         
# python3 -m unittest tests/test_upload_validator.py
            
class TestUploadValidator(unittest.TestCase):
    
    def setUp(self):
        self.assertEqual.__self__.maxDiff = None
    
    def test_validate_filenames(self):
        
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
        
        # alt + z to wrap text
        response, status_code = rv_tools_validator.get_filenames_response(flask_request)
        # print(response)   
        self.assertEqual(status_code, 200)
        filenames_response = {'status': 'success', 'message': 'Filenames are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'message': 'Filename is valid'}, {'status': 'fail', 'filename': 'randomfile.pdf', 'message': 'File must contain at least one of the following keywords: RV, Tools'}, {'status': 'ignored', 'filename': 'skip_this_file.csv', 'message': 'Filename is ignored'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}
        self.assertDictEqual(response, filenames_response)
    
        response, status_code = rv_tools_validator.get_file_objects_response(flask_request)
        self.assertEqual(status_code, 200)
        # print(response)  
        file_objects_response = {'status': 'success', 'message': 'Files are valid', 'validation': [{'status': 'success', 'filename': 'rvtools.xlsx', 'filepath': '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/rvtools.xlsx', 'message': 'Filename is valid'}, {'status': 'success', 'filename': 'rv_tools.xlsx', 'filepath': '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/rv_tools.xlsx', 'message': 'Filename is valid'}], 'quota': {'status': 'success', 'message': 'Quota within limits'}}
        self.assertDictEqual(response, file_objects_response)
        
        file_paths = rv_tools_validator.get_filepaths_from_objects_response(file_objects_response)
        
        [self.assertEqual(os.path.exists(fp), True) for fp in file_paths]
         
        
    