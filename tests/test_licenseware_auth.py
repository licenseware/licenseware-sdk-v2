import os
import unittest
        
# python3 -m unittest tests/test_licenseware_auth.py


class TestAuth(unittest.TestCase):
    
    def setUp(self):
        
        os.environ["LWARE_IDENTITY_USER"] = "LWARE_IDENTITY_USER"
        os.environ["LWARE_IDENTITY_PASSWORD"] = "LWARE_IDENTITY_PASSWORD"
        os.environ["AUTH_SERVICE_URL"] = "AUTH_SERVICE_URL"
        os.environ["AUTH_SERVICE_MACHINES_URL_PATH"] = "AUTH_SERVICE_MACHINES_URL_PATH"
        os.environ["AUTH_SERVICE_USERS_URL_PATH"] = "AUTH_SERVICE_USERS_URL_PATH"
        os.environ["AUTH_TOKEN"] = "AUTH_TOKEN"
        os.environ["TENANT_ID"] = "TENANT_ID"
        os.environ["APP_AUTHENTICATED"] = "APP_AUTHENTICATED"
        os.environ["AUTH_TOKEN_DATETIME"] = "AUTH_TOKEN_DATETIME"
        

    def tearDown(self):
        
        os.environ.pop("LWARE_IDENTITY_USER")
        os.environ.pop("LWARE_IDENTITY_PASSWORD")
        os.environ.pop("AUTH_SERVICE_URL")
        os.environ.pop("AUTH_SERVICE_MACHINES_URL_PATH")
        os.environ.pop("AUTH_SERVICE_USERS_URL_PATH")
        os.environ.pop("AUTH_TOKEN")
        os.environ.pop("TENANT_ID")
        os.environ.pop("APP_AUTHENTICATED")
        os.environ.pop("AUTH_TOKEN_DATETIME")
        
        
    def test_envs_are_set(self):
        self.assertEqual(os.getenv("LWARE_IDENTITY_USER"), "LWARE_IDENTITY_USER")
        
        
    def test_verify_envs_dataclasss(self):
    
        # Environment variables must be set first before calling
        from app.licenseware.common.constants import envs 

        self.assertEqual(envs.LWARE_USER, "LWARE_IDENTITY_USER")
        self.assertEqual(envs.LWARE_PASSWORD, "LWARE_IDENTITY_PASSWORD")
        self.assertEqual(envs.AUTH_BASE_URL, "AUTH_SERVICE_URL")
        self.assertEqual(envs.AUTH_MACHINES_ROUTE, "AUTH_SERVICE_MACHINES_URL_PATH")
        self.assertEqual(envs.AUTH_USERS_ROUTE, "AUTH_SERVICE_USERS_URL_PATH")
        self.assertEqual(envs.AUTH_TOKEN, "AUTH_TOKEN")
        self.assertEqual(envs.TENANT_ID, "TENANT_ID")
        self.assertEqual(envs.APP_AUTHENTICATED, True)
        self.assertEqual(envs.AUTH_TOKEN_DATETIME, "AUTH_TOKEN_DATETIME")
        self.assertEqual(envs.AUTH_USERS_URL, 'AUTH_SERVICE_URLAUTH_SERVICE_USERS_URL_PATH')
        self.assertEqual(envs.AUTH_MACHINES_URL, 'AUTH_SERVICE_URLAUTH_SERVICE_MACHINES_URL_PATH')
        
    def test_auth_create(self):
        
        from app.licenseware.auth import Authenticator
        
        
    def test_auth_login(self):
        
        from app.licenseware.auth import Authenticator
        
        response = Authenticator.connect()
        
        print(response)
        
        
        
        
        
    
