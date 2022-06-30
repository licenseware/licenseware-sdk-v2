import time
import unittest
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.miscellaneous import set_environment_variables
from licenseware.utils.dramatiq_redis_broker import celery

# python3 -m unittest tests/test_flask_celery.py


@celery.task
def processing_func(param1: str, param2: dict):
    print("Processing...", param1, param2)
    time.sleep(3)
    print("Done!")


class TestFlaskCelery(unittest.TestCase):

    # def setUp(self) -> None:
    #     self.host = "redis"
    #     self.port = "6379"
    #     self.db  = "1"
    #     self.password = ""
        
    #     set_environment_variables(
    #         envs=dict(
    #             REDIS_DB="1",
    #             REDIS_HOST="redis",
    #             REDIS_PASSWORD="",
    #             REDIS_PORT="6379",
    #         )
    #     )

    def test_simple_celery(self):

        # @celery.task
        # def processing_func(param1: str, param2: dict):
        #     print("Processing...", param1, param2)
        #     time.sleep(3)
        #     print("Done!")

        print(processing_func)

        processing_func.delay("args", {"key": "value"})
        


    # def test_flask_celery(self):

    #     @broker.actor
    #     def processing_func(param1: str, param2: dict):
    #         print("Processing...", param1, param2)
    #         time.sleep(3)
    #         print("Done!")

    #     print(processing_func)

    #     processing_func.send("args", {"key": "value"})

        


