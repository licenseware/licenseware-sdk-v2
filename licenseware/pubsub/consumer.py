import json
from typing import Callable

from confluent_kafka import Consumer as KafkaConsumer

from licenseware.pubsub.types import EventType


class Consumer:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer
        self.event_dispacher = dict()

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])
        return self

    def dispatch(self, event_type: EventType, event_handler: Callable):
        self.event_dispacher[event_type] = event_handler
        return self

    def listen(self):

        try:

            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue

                print("Received message: {}".format(msg.value()))

                data = json.loads(msg.value().decode("utf-8"))

                event_type_found = "event_type" in data.keys()
                tenant_id_found = "tenant_id" in data.keys()

                if event_type_found and tenant_id_found:
                    print(
                        "Consumer error: `event_type` and `tenant_id` not found on message."
                    )
                    continue

                self.event_dispacher[data["event_type"]](**data)

        except Exception as err:
            print(err)
            self.consumer.close()
