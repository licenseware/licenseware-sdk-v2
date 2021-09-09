import os
import shutil
import unittest
from licenseware.cli.cli import make_sdk_docs, make_docs
        
# python3 -m unittest tests/test_make_docs.py


class TestSDKDocs(unittest.TestCase):
    
    def setUp(self):
        if not os.path.exists('app'): 
            os.makedirs('app')
            with open('app/__init__.py', 'w') as f:
                f.write("import os")
    
    def tearDown(self):
        if os.path.exists('app'):
            shutil.rmtree('app') 
            shutil.rmtree('docs') 
        
    def test_make_sdk_docs(self):
        make_sdk_docs()
        assert os.path.exists('docs')
        
    def test_make_app_docs(self):
        make_docs()
        assert os.path.exists('docs')
        
        
    