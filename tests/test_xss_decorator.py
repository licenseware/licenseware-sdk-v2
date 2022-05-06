import unittest
from licenseware.decorators.xss_decorator import xss_security, xss_validator


# python3 -m unittest tests/test_xss_decorator.py


class TestXSSDecorator(unittest.TestCase):

    def test_xss_validator(self):

        data = {
            "test": 1
        }

        xss_validator(data)



