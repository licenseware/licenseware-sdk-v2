import os
from .flask_celery import CeleryBroker
# from .flask_dramatiq import Dramatiq
from celery import Celery

# Dramatiq
# broker = Dramatiq(
#     host=os.getenv('REDIS_HOST', 'localhost'),
#     port=os.getenv('REDIS_PORT', 6379),
#     db=os.getenv('REDIS_DB', 0),
#     password=os.getenv('REDIS_PASSWORD', None)
# )


# Celery


celery = Celery(
    broker=f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}/{os.getenv('REDIS_DB', 0)}",
    include=["tasks"]

)

broker = CeleryBroker(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=os.getenv('REDIS_DB', 0),
    password=os.getenv('REDIS_PASSWORD', None)
)

