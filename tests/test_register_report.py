import unittest
from licenseware.registry_service import register_report


# python3 -m unittest tests/test_register_report.py


payload = {'app_id': 'acmtifmp', 'report_id': 'acmtvirtualization_details', 'name': 'Virtualization Details', 'description': 'This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.', 'flags': [], 'url': 'http://localhost:5000/acmtifmp/reports/acmtvirtualization_details', 'report_components': [{'title': 'Overview', 'order': 1, 'component_id': 'virtual_overview', 'url': 'http://localhost:5000/acmtifmp/reports/acmtvirtualization_details/virtual_overview', 'style_attributes': {'width': '1/3'}, 'attributes': {'series': [{'value_description': 'Number of devices', 'value_key': 'number_of_devices', 'icon': 'ServersIcon'}, {'value_description': 'Number of databases', 'value_key': 'number_of_databases', 'icon': 'DatabaseIconRounded'}]}, 'filters': [{'column': 'device_name', 'allowed_filters': ['equals', 'contains', 'in_list'], 'visible_name': 'Device Name'}, {'column': 'database_name', 'allowed_filters': ['equals', 'contains', 'in_list'], 'visible_name': 'Database Name'}], 'type': 'summary'}], 'connected_apps': ['ifmp-service'], 'filters': [{'column': 'device_name', 'allowed_filters': ['equals', 'contains', 'in_list'], 'visible_name': 'Device Name'}, {'column': 'database_name', 'allowed_filters': ['equals', 'contains', 'in_list'], 'visible_name': 'Database Name'}]}


class TestRegisterReport(unittest.TestCase):
    
    def test_register_uploader(self):
        response, status_code = register_report(**payload)
        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], "success")
        self.assertIn("ifmp/", str(response))