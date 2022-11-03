# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import json
import traceback
from typing import Callable

from licenseware.utils.logger import log

from .types import EventType, TopicType


class Consumer:
    def __init__(self, consumer_factory: Callable, config: Config):
        self.config = config
        self.consumer_factory = consumer_factory
        self.consumer = consumer_factory(config)
        self.event_dispacher = dict()
        self._allowed_topics = TopicType().dict().values()
        self._subscribed = False

    def subscribe(self, topic: str):
        assert topic in self._allowed_topics
        self.consumer.subscribe([topic])
        self._subscribed = True
        return self

    def dispatch(self, event_type: EventType, event_handler: Callable):
        if not self._subscribed:
            raise Exception("Please subscribe to at least one topic/channel")
        self.event_dispacher[event_type] = event_handler
        return self

    def listen(self):

        try:

            log.info("Listening to stream...")

            while True:

                msg = self.consumer.poll(self.config.KAFKA_CONSUMER_POLL)

                if msg is None:
                    continue
                if msg.error():
                    log.error("Consumer error: {}".format(msg.error()))
                    continue

                event = json.loads(msg.value().decode("utf-8"))

                if "event_type" not in event.keys():
                    log.error(
                        f"Can't dispach message without any `event_type` set \n Ignoring message: {msg.value()}"
                    )
                    continue

                if event["event_type"] not in self.event_dispacher:
                    log.error(
                        f"Can't dispach `event_type`:{event['event_type']}. \
                        Please `dispatch` a handler for this event type.  \n Ignoring message: {msg.value()}"
                    )
                    continue

                self.event_dispacher[event["event_type"]](event)

        except Exception as err:
            log.warning(traceback.format_exc())
            log.error(
                f"Got the following error on consumer: \n {err} \n\n Reconecting..."
            )
            self.consumer.close()
            self.consumer = self.consumer_factory(self.config)
            self.listen()
