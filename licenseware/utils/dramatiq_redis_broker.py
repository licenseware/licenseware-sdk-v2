from flask_dramatiq import Dramatiq

broker = Dramatiq(broker_cls='dramatiq.brokers.redis:RedisBroker')
