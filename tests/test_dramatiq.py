import os
import unittest

from licenseware.utils.flask_dramatiq import Dramatiq

# python3 -m unittest tests/test_dramatiq.py


class TestDramatiq(unittest.TestCase):
    def test_dramatiq(self):

        os.environ["USE_BACKGROUND_WORKER"] = "false"

        broker = Dramatiq(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=os.getenv("REDIS_PORT", 6379),
            db=os.getenv("REDIS_DB", 0),
            password=os.getenv("REDIS_PASSWORD", None),
        )

        def processingFunc():
            print("processsing something")

        self.assertEqual(processingFunc.__name__, "processingFunc")

        @broker.actor
        def processingFuncDecorated():
            print("processsing something")

        self.assertEqual(processingFuncDecorated.fn.__name__, "processingFuncDecorated")
