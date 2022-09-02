import unittest

from main import app

from licenseware.app_builder.app_builder import base_paths
from licenseware.common.constants import envs
from licenseware.utils.logger import log

from . import headers, tenant_id

# python3 -m unittest tests/test_app_builder_routes.py


prefix = envs.APP_ID


class TestAppBuilderRoutes(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_app_activation_path(self):
        response = self.app.get(
            prefix + base_paths.app_activation_path, headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_editable_tables_path(self):
        response = self.app.get(
            prefix + base_paths.editable_tables_path, headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_refresh_registration_path(self):
        response = self.app.get(
            prefix + base_paths.refresh_registration_path, headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_register_app_path(self):
        response = self.app.get(prefix + base_paths.register_app_path, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_tenant_registration_path(self):
        response = self.app.get(
            prefix + base_paths.tenant_registration_path,
            query_string={"tenant_id": tenant_id},
            headers=headers,
        )

        log.debug(response.data)

        self.assertEqual(response.status_code, 200)
