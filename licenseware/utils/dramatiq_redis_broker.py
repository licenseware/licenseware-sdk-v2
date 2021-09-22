import os
from .flask_dramatiq import Dramatiq


broker = Dramatiq(
    url = os.getenv('REDIS_CONNECTION_STRING')
)