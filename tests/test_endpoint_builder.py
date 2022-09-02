import unittest

from licenseware.endpoint_builder import EndpointBuilder
from licenseware.utils.logger import log

# python3 -m unittest tests/test_endpoint_builder.py


class TestEndpointBuilder(unittest.TestCase):
    def test_endpoint_builder(self):
        def get_custom_data_from_mongo(flask_request):
            """Custom documentation"""

            # Some logic here

            return "Some data"

        custom_endpoint = EndpointBuilder(handler=get_custom_data_from_mongo)

        self.assertEqual(custom_endpoint.docid, """ Custom documentation """)
        self.assertEqual(custom_endpoint.http_path, "/get_custom_data_from_mongo")
        self.assertEqual(custom_endpoint.http_method, "GET")

        log.debug(vars(custom_endpoint))
        # log.debug(dir(custom_endpoint))
