import unittest
from app.licenseware.registry_service import register_report


# python3 -m unittest tests/test_register_report.py


payload = {'app_id': 'ifmp', 'report_id': 'virtualization_details', 'name': 'Virtualization Details', 'description': 'This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.', 'flags': [], 'report_url': 'http://localhost:5000/ifmp/reports/virtualization_details', 'report_components': [{'title': 'Overview', 'order': 1, 'url': 'http://localhost:5000/ifmp/reports/virtualization_details/virtual_overview', 'component_id': 'virtual_overview', 'icon': 'ServersIcon', 'type': 'summary', 'style_attributes': {'width': '1/3'}, 'attributes': {'series': [{'name': 'Number of devices', 'machine_name': 'number_of_devices', 'icon': 'ServersIcon'}, {'name': 'Number of databases', 'machine_name': 'number_of_databases', 'icon': 'DatabaseIconRounded'}]}}], 'connected_apps': ['ifmp-service']}



class TestRegisterReport(unittest.TestCase):
    
    def test_register_uploader(self):
        response, status_code = register_report(**payload)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], "success")
        self.assertIn("ifmp/", str(response))