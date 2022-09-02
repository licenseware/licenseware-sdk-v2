import os
import shutil
import unittest

from licenseware.cli.aws_cloud_formation import create_aws_cloud_formation
from licenseware.cli.github_workflows import create_github_workflows

# python3 -m unittest tests/test_devops_folders_files_creation.py


class TestDevOpsFiles(unittest.TestCase):
    def tearDown(self):

        if os.path.exists(".github"):
            shutil.rmtree(".github")

        if os.path.exists("cloudformation-templates"):
            shutil.rmtree("cloudformation-templates")

    def test_git_workflow_files(self):

        create_github_workflows("dashboard-service")

        self.assertTrue(os.path.exists(".github/workflows"))
        self.assertEqual(len(os.listdir(".github/workflows")), 4)

    def test_aws_cloud_formation(self):

        create_aws_cloud_formation("dashboard-service")

        self.assertTrue(os.path.exists("cloudformation-templates"))
        self.assertEqual(len(os.listdir("cloudformation-templates")), 2)
