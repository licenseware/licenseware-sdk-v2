# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

from confluent_kafka import Producer as KafkaProducer

from licenseware.pubsub.producer import Producer


def get_kafka_producer(config: Config):
    producer_client_factory = lambda cfg: KafkaProducer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_producer = Producer(producer_client_factory, config)
    return kafka_producer
