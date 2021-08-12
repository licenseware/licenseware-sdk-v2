import unittest
from app.licenseware.registry_service import register_uploader


# python3 -m unittest tests/test_register_uploader.py 


payload = {'name': 'RVTools', 
           'description': 'XLSX export from RVTools after scanning your Vmware infrastructure.', 
           'accepted_file_types': ['.xls', '.xlsx'], 
           'app_id': 'ifmp', 
           'uploader_id': 'rv_tools_file', 
           'flags': [], 
           'status': 'idle', 
           'icon': 'default.png', 
           'upload_url': 'http://localhost:5000/ifmp/uploads/rv_tools_file/files', 
           'upload_validation_url': 'http://localhost:5000/ifmp/uploads/rv_tools_file/validation', 
           'quota_validation_url': 'http://localhost:5000/ifmp/uploads/quota/rv_tools_file', 
           'status_check_url': 'http://localhost:5000/ifmp/uploads/rv_tools_file/status'}


class TestRegisterUploader(unittest.TestCase):
    
    def test_register_uploader(self):
        response, status_code = register_uploader(**payload)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], "success")