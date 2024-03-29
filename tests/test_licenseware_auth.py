import os
import unittest

from licenseware.auth import Authenticator
from licenseware.common.constants import envs

# python3 -m unittest tests/test_licenseware_auth.py


class TestAuth(unittest.TestCase):
    def test_envs_are_set(self):
        self.assertEqual(os.getenv("LWARE_IDENTITY_USER"), "John")

    def test_envs_dataclass_loaded_environ(self):

        self.assertEqual(envs.LWARE_USER, "John")
        self.assertEqual(envs.LWARE_PASSWORD, "secret")
        self.assertEqual(envs.AUTH_MACHINES_URL, "http://localhost:5000/auth/machines")

    def test_envs_dataclass_dynamic(self):

        self.assertEqual(os.getenv("SOMETHING"), None)
        os.environ["SOMETHING"] = "some value"
        self.assertEqual(os.getenv("SOMETHING"), "some value")
        os.environ.pop("SOMETHING")

    def test_auth(self):

        Authenticator.connect()

        self.assertEqual(envs.get_auth_token(), "long_auth_token")
        self.assertEqual(envs.app_is_authenticated(), True)
        self.assertIsNotNone(envs.get_auth_token_datetime())
