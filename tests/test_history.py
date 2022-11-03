import os
import traceback
import unittest
import uuid

from licenseware import history
from licenseware.constants.worker_event_type import WorkerEvent
from licenseware.dependencies import get_kafka_producer
from settings import config

# python3 -m unittest tests/test_history.py


class TestHistory(unittest.TestCase):
    def test_history(self):
        class ProcessingUploaderIdEvent:
            def __init__(self, event: dict) -> None:
                self.event = WorkerEvent(**event)
                self.filepath = self.event.filepaths[0]
                self.filename = os.path.basename(self.event.filepaths[0])
                self.producer = get_kafka_producer(config)

            @history.log
            def some_func(self):
                return "ok"

        event = {
            "tenant_id": str(uuid.uuid4()),
            "authorization": str(uuid.uuid4()),
            "uploader_id": "rv_tools",
            "uploader_name": "RvTOOLS",
            "event_id": str(uuid.uuid4()),
            "app_id": "ifmp-service",
            "app_name": "Infra App",
            "filepaths": ["tests/test_data/comma.csv"],
        }

        assert ProcessingUploaderIdEvent(event).some_func() == "ok"
