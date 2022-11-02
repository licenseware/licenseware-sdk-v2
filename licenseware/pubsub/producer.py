# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import json
from typing import Callable

from licenseware.utils.logger import log

from .types import EventType, TopicType


class Producer:
    def __init__(
        self,
        producer_factory: Callable,
        config: Config,
        delivery_report: Callable = None,
    ):
        self.config = config
        self.producer_factory = producer_factory
        self.producer = producer_factory(config)
        self.delivery_report = delivery_report
        self._allowed_events = EventType().dict().values()
        self._allowed_topics = TopicType().dict().values()

    def _checks(self, topic, data):

        assert topic in self._allowed_topics, "This is not an allowed topic/channel."
        assert isinstance(data, dict), "Must be a `dict` type"
        assert "event_type" in data, "Field `event_type` not found"
        if data["event_type"] not in self._allowed_events:
            log.info(
                f"Unkown EventType: '{data['event_type']}'. Make sure to add it to `licenseware.pubsub.types`"
            )

    def publish(
        self,
        topic: TopicType,
        data: dict,
        delivery_report: Callable = None,
        fresh_connect: bool = False,
    ):

        if fresh_connect:
            self.producer = self.producer_factory(self.config)

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
            log.error("Message delivery failed: {}".format(err))
            raise Exception("Lost connection to kafka...")
        else:
            log.success(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )
