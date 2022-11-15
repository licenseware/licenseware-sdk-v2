# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

from confluent_kafka import Consumer as KafkaConsumer

from licenseware.pubsub.consumer import Consumer


def get_kafka_consumer(config: Config):
    consumer_client_factory = lambda cfg: KafkaConsumer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "group.id": cfg.APP_ID,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_consumer = Consumer(consumer_client_factory, config)
    return kafka_consumer
