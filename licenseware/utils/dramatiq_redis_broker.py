import os
from .flask_dramatiq import Dramatiq


broker = Dramatiq(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB'),
    password=os.getenv('REDIS_PASSWORD')
)


