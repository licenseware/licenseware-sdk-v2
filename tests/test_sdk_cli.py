import os
import shutil
import unittest
from licenseware.cli import app
from licenseware.cli.app_dirs import app_path
from typer.testing import CliRunner

from licenseware.utils.logger import log

# python3 -m unittest tests/test_sdk_cli.py




class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.runner = CliRunner()
        
    # def tearDown(self):
    #     shutil.rmtree(app_path)
    
    def test_create_app(self):
        result = self.runner.invoke(app, ["new-app"])
        log.debug(result.stdout)
        assert result.exit_code == 0
        assert os.path.exists(app_path)
        
    
    def test_create_report(self):
        result = self.runner.invoke(app, ["new-report", "virtualization_details"])
        log.debug(result.stdout)
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(app_path, 'reports', 'virtualization_details'))
        
    
    def test_create_report_component(self):
        result = self.runner.invoke(app, ["new-report-component", "virtual_overview", "summary"])
        log.debug(result.stdout)
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(app_path, 'report_components', 'virtual_overview'))
        
        
    def test_create_uploader(self):
        result = self.runner.invoke(app, ["new-uploader", "rv_tools"])
        log.debug(result.stdout)
        assert result.exit_code == 0
        assert os.path.exists(os.path.join(app_path, 'uploaders', 'rv_tools'))
        
        
        


