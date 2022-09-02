import json
from typing import Callable

from confluent_kafka import Producer as KafkaProducer

from .types import EventType, TopicType


class Producer:
    def __init__(self, producer: KafkaProducer, delivery_report: Callable = None):
        self.producer = producer
        self.delivery_report = delivery_report
        self._allowed_events = EventType.dict().values()
        self._allowed_topics = TopicType.dict().values()

    def _checks(self, topic, data):

        assert isinstance(topic, TopicType)
        assert isinstance(data, dict)
        assert "event_type" in data.keys()
        assert "tenant_id" in data.keys()
        assert topic in self._allowed_topics
        assert data["event_type"] in self._allowed_events

    def publish(self, topic: TopicType, data: dict, delivery_report: Callable = None):

        self._checks(topic, data)
        databytes = json.dumps(data).encode("utf-8")

        self.producer.poll(0)
        self.producer.produce(
            topic, databytes, callback=delivery_report or self.delivery_report
        )
        self.producer.flush()

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))
