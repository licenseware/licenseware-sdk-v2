import os
import unittest
from licenseware.utils.logger import log

from licenseware.cli.root_files import create_root_files, resources_filenames


# python3 -m unittest tests/test_create_root_files.py



class TestRootFiles(unittest.TestCase):
    
    def test_create_root_files(self):
        
        create_root_files()
        
        for rname, fname in resources_filenames.items():  
            assert os.path.exists(fname)
        
        
        
        