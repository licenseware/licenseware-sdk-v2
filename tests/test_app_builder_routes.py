import unittest
from app.licenseware.utils.logger import log
from app.licenseware.app_builder.app_builder import base_paths
from main import app
 
 
# python3 -m unittest tests/test_app_builder_routes.py
 
headers = {
    'Tenantid': 'TheTenantid',
    'Authorization': 'TheAuthorization' 
}

prefix = '/ifmp'
pathto = lambda route: prefix + route



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
        response = self.app.get(pathto(base_paths.app_activation_path), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_app_init_route(self):
        response = self.app.get(pathto(base_paths.register_app_path), headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_refresh_registration_route(self):
        response = self.app.get(pathto(base_paths.refresh_registration_path), headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_editable_tables_route(self):
        response = self.app.get(pathto(base_paths.editable_tables_path), headers=headers)
        self.assertEqual(response.status_code, 200)
        
        
        
        
        
 