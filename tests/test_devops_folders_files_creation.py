import unittest
from licenseware.cli.github_workflows import create_github_workflows

import os
import shutil

# python3 -m unittest tests/test_devops_folders_files_creation.py



class TestDevOpsFiles(unittest.TestCase):
    
    def tearDown(self):
        shutil.rmtree(".github")
    
    
    def test_git_workflow_files(self):
        
        create_github_workflows('odb')
        
        self.assertTrue(os.path.exists('.github/workflows'))
        self.assertEqual(len(os.listdir('.github/workflows')), 3)
        
        
        