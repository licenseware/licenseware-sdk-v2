import unittest

from licenseware.registry_service import register_component

# python3 -m unittest tests/test_register_report_component.py


payload = {
    "data": [
        {
            "app_id": "odb_222",
            "component_id": "top_usage_databases_222",
            "url": "http://localhost:5000/odb/report_components/top_usage_databases",
            "order": 20,
            "style_attributes": {"width": "full"},
            "attributes": {
                "series": [
                    {"xaxis_description": "Database Name", "xaxis_key": "database"},
                    {
                        "yaxis_description": "Processor Licenses Required",
                        "yaxis_key": "oracle_processors_required",
                    },
                ]
            },
            "title": "Top 10 High Usage Databases",
            "type": "bar_vertical",
            "filters": None,
        }
    ]
}


class TestRegisterReport(unittest.TestCase):
    def test_register_uploader(self):

        data = payload["data"][0]

        data["component_type"] = data["type"]

        response, status_code = register_component(**data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
