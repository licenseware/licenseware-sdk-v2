import unittest
from app.licenseware.registry_service import register_app


# python3 -m unittest tests/test_register_app.py 


payload = {'app_id': 'ifmp', 'name': 'Infrastructure Mapper', 'activated_tenants': [], 'tenants_with_data': [], 'description': 'Overview of devices and networks', 'flags': ['beta'], 'icon': 'default.png', 'refresh_registration_url': 'http://localhost:5000/ifmp/register_all', 'app_activation_url': 'http://localhost:5000/ifmp/app/init', 'editable_tables_url': 'http://localhost:5000/ifmp/editable_tables', 'history_report_url': 'http://localhost:5000/ifmp/reports/history_report', 'tenant_registration_url': 'http://localhost:5000/ifmp/tenant_registration_url'}



class TestRegisterApp(unittest.TestCase):
    
    def test_register_app(self):
        response, status_code = register_app(**payload)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], "success")