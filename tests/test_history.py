import os
import unittest
import uuid

from licenseware import history
from licenseware.constants.worker_event_type import WorkerEvent
from licenseware.dependencies import get_kafka_producer
from licenseware.history.schemas import EventTypes
from settings import config

# python3 -m unittest tests/test_history.py


class TestHistory(unittest.TestCase):
    def test_history(self):
        class ProcessingUploaderIdEvent:
            def __init__(self, event: dict) -> None:
                self.raw_event = event
                self.event = WorkerEvent(**event)
                self.filepath = self.event.filepaths[0]
                self.filename = os.path.basename(self.event.filepaths[0])
                self.producer = get_kafka_producer(config)
                self.event_type = EventTypes.PROCESSING_DETAILS

            @history.log
            def some_func(self):
                return "ok"

            def publishing_some_entities(self):

                history.publish_entities(
                    self.producer,
                    self.event,
                    entities=["some-entiry-here"],
                )

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

        p = ProcessingUploaderIdEvent(event)
        # assert p.some_func() == "ok"
        assert p.publishing_some_entities() == "ok"
