import unittest

from licenseware.decorators.xss_decorator import xss_validator

# python3 -m unittest tests/test_xss_decorator.py


class TestXSSDecorator(unittest.TestCase):
    def test_xss_validator(self):

        data = {
            "integration_id": "lansweeper",
            "updated_at": "2022-05-17T04:46:12.205750",
            "tenant_id": "437fe9d0-39c7-55bd-b12d-95025991cc4a",
            "logo": None,
            "description": "Integration with Lansweeper API's",
            "test_url": "https://www.lansweeper.com/",
            "inputs": [
                {
                    "label": "Lansweeper Password",
                    "id": "lansweeper_password",
                    "value": "https://lansweeper.123.com",
                    "error_message": "URL should start with https://lansweeper.123.com",
                    "rules": None,
                    "type": "password",
                }
            ],
            "name": "Lansweeper",
            "status": "disabled",
            "apps": [
                {
                    "app_id": "odb-service",
                    "name": "Oracle Database",
                    "description": "Analyse oracle database",
                    "integration_id": "lansweeper",
                    "imported_data": ["oracle_databases"],
                    "exported_data": ["reports"],
                    "triggers": [
                        "database_created",
                        "database_deleted",
                        "< HTTP-EQUIV charset=network_scan",
                    ],
                }
            ],
        }

        xss_validator(data)

        # with self.assertRaises(Exception):
        #     xss_validator(data)

        # data = {
        #     "test": "< good/>"
        # }

        # xss_validator(data)
