from logging import log
import re
import unittest
from marshmallow import Schema, fields
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.namespace_generator import SchemaNamespace
from main import app


# python3 -m unittest tests/test_namespace_generator.py


class TestNamespaceGenerator(unittest.TestCase):
    
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    
    def test_namespace_generator(self):
        
        
        class UserSchema(Schema):
            class Meta:
                collection_name = envs.MONGO_COLLECTION_DATA_NAME
                
            name = fields.Str(required=True)
            occupation = fields.Str(required=True)
        
    
        UserNs = SchemaNamespace(
            schema=UserSchema
        )
        
        log.debug(UserNs)
        
        