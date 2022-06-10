import unittest


# python3 -m unittest tests/test_config.py

class TestConfig(unittest.TestCase):

    def test_config(self):

        from licenseware.common.constants import envs

        print(envs.APP_ID)
        print(envs.ENVIRONMENT)