import unittest
from app.licenseware.registry_service import register_app


# python3 -m unittest tests/test_register_app.py 


payload = {'id': 'ifmp', 'name': 'Infrastructure Mapper', 'activated_tenants': [], 'tenants_with_data': [], 'description': 'Overview of devices and networks', 'flags': ['beta'], 'icon': 'default.png', 'refresh_registration_url': 'http://localhost:5000/register_all', 'app_activation_url': 'http://localhost:5000/app/init', 'editable_tables_url': 'http://localhost:5000/editable_tables', 'history_report_url': 'http://localhost:5000/reports/history_report', 'tenant_registration_url': 'http://localhost:5000/tenant_registration_url'}



class TestRegisterApp(unittest.TestCase):
    
    def test_register_app(self):
        response, status_code = register_app(**payload)
        self.assertEqual(status_code, 200)
        self.assertEquals(response['status'], "success")