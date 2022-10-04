from confluent_kafka import Producer as KafkaProducer

from licenseware.pubsub.producer import Producer


def get_kafka_producer(config):
    producer_client_factory = lambda cfg: KafkaProducer(
        {
            "bootstrap.servers": cfg.KAFKA_BROKER_URL,
            "security.protocol": cfg.KAFKA_SECURITY_PROTOCOL,
        }
    )
    kafka_producer = Producer(producer_client_factory, config)
    return kafka_producer
