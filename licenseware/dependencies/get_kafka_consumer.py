from confluent_kafka import Consumer as KafkaConsumer

from licenseware.pubsub.consumer import Consumer


def get_kafka_consumer(config):
    consumer_client_factory = lambda cfg: KafkaConsumer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "group.id": cfg.APP_ID,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_consumer = Consumer(consumer_client_factory, config)
    return kafka_consumer
