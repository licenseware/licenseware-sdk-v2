import unittest

from licenseware.registry_service import register_app

# python3 -m unittest tests/test_register_app.py


payload = {
    "data": [
        {
            "app_id": "odb_222",
            "name": "Oracle Database Manager",
            "tenants_with_app_activated": ["3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a"],
            "tenants_with_data_available": [],
            "description": "This App handles Oracle Database data, identifies running options and features and reconcilies with infrastructure data for a complete Oracle deployment.",
            "flags": ["beta"],
            "icon": "default.png",
            "refresh_registration_url": "http://localhost:5000/odb/refresh_registration",
            "app_activation_url": "http://localhost:5000/odb/activate_app",
            "editable_tables_url": "http://localhost:5000/odb/editable_tables",
            "history_report_url": "http://localhost:5000/odb/reports/history_report",
            "tenant_registration_url": "http://localhost:5000/odb/register_tenant",
        }
    ]
}


class TestRegisterApp(unittest.TestCase):
    def test_register_app(self):

        data = payload["data"][0]

        data["activated_tenants"] = data.pop("tenants_with_app_activated")
        data["tenants_with_data"] = data.pop("tenants_with_data_available")

        response, status_code = register_app(**data)

        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
