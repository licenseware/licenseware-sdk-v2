import unittest
from licenseware.decorators.xss_decorator import xss_security, xss_validator


# python3 -m unittest tests/test_xss_decorator.py


class TestXSSDecorator(unittest.TestCase):

    def test_xss_validator(self):

        data = {
            "test": "<img onerror=alert(bad)>"
        }

        with self.assertRaises(Exception):
            xss_validator(data)


        data = {
            "test": "< good/>"
        }

        xss_validator(data)

