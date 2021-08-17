import unittest
from app.licenseware.utils.logger import log
from main import app
 
 
# python3 -m unittest tests/test_app_builder_routes.py
 
headers = {
    'Tenantid': 'TheTenantid',
    'Authorization': 'TheAuthorization' 
}

prefix = '/ifmp/v1'
pathto = lambda route: prefix + route


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
        
        
        
 