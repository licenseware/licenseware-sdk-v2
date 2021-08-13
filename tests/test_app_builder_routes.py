import unittest
from main import app
 
 
# python3 -m unittest tests/test_app_builder_routes.py
 
headers = {
    'Tenantid': 'TheTenantid',
    'Authorization': 'TheAuthorization' 
}

prefix = '/ifmp/v1'
pathto = lambda route: prefix + route

uploader_id = 'rv_tools'

upload_validation_path = f"/uploads/{uploader_id}/validation"
upload_path = f"/uploads/{uploader_id}/files"
quota_validation_path = f"/uploads/quota/{uploader_id}"
status_check_path = f"/uploads/{uploader_id}/status"



#TODO check the altered data by the endpoints

 
class TestAppBuilderRoutes(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        
    def tearDown(self):
        return super().tearDown()
             
             
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_app_route(self):
        response = self.app.get(pathto('/app'), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_app_init_route(self):
        response = self.app.get(pathto('/app/init'), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_register_all_route(self):
        response = self.app.get(pathto('/register_all'), headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_editable_tables_route(self):
        response = self.app.get(pathto('/editable_tables'), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_uploads_filenames_validation_route(self):
        
        url = pathto(upload_validation_path)
        
        response = self.app.post(
            url, 
            headers=headers,
            json=['rvtools.xlsx', "rv_tools.xlsx", 'randomfile.pdf']
        )
        
        self.assertEqual(response.status_code, 200)
    
 