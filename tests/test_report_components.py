import unittest

from main import app

from app.licenseware.app_builder import AppBuilder
from app.licenseware.report_components import SummaryReportComponent
from app.licenseware.report_components import style_props
from app.licenseware.common.constants import icons
from app.licenseware.report_builder import ReportBuilder
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs

from . import headers

# python3 -m unittest tests/test_report_components_data_url.py

 
class TestReportComponentsRoutes(unittest.TestCase):
    
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    def tearDown(self):
        ifmp_app = None
        report_obj = None
        component_obj = None
        
        
    def test_report_metadata(self):
        
        report_path = envs.APP_ID + envs.REPORT_PATH + report_obj.report_path
        
        log.debug(report_path)
        
        response = self.app.get(report_path, headers=headers)
        
        log.debug(response.data)
        
        self.assertEqual(response.status_code, 200)
        
        
    def test_component_ids_urls(self):
        
        self.assertFalse(report_obj.report_url.endswith(component_obj.component_id))
    
        result = component_obj.get_component_data('tenant_id', {'filters': None})
        self.assertEqual(result, ['mongo db aggregation pipeline'])
        
 
 