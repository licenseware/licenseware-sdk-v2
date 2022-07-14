from functools import partial, wraps

from licenseware.common.constants import envs
from licenseware.utils.logger import log

if envs.BROKER_IS_CELERY:
    from celery import Celery

    celery_app = Celery(
        envs.CELERY_APP_NAME,
        broker=envs.CELERY_BROKER_URI,
        backend=envs.CELERY_RESULT_BACKEND,
        broker_transport_options=envs.celery_broker_transport_options(),
        kafka_consumer_config=envs.celery_kafka_consumer_config(),
        broker_connection_max_retries=envs.CELERY_BROKER_CONN_MAX_RETRIES,
        task_serializer=envs.CELERY_SERIALIZER,
        task_default_rate_limit=envs.CELERY_TASK_DEFAULT_RATE_LIMIT,
        task_compression=envs.CELERY_COMPRESSION,
        result_compression=envs.CELERY_COMPRESSION,
        result_serializer=envs.CELERY_SERIALIZER,
        accept_content=[envs.CELERY_SERIALIZER],
    )

    # backwards compatibility
    @wraps(celery_app.send_task)
    def send(name, *args, **kwargs):
        log.debug("*" * 80)
        log.info(name)
        log.debug(len(args))
        log.debug(len(kwargs))
        celery_app.send_task(name, args=args, kwargs=kwargs)
        log.info("done sending!")

    @wraps(celery_app.task)
    def task(fn=None, *args, **kwargs):
        if fn is None:
            return partial(task)

        wrapped = celery_app.task(fn, *args, **kwargs)
        wrapped.send = partial(send, wrapped.name)
        return wrapped

    broker = celery_app
    broker.actor = task
    broker.init_app = lambda _: celery_app

else:
    from .flask_dramatiq import Dramatiq

    broker = Dramatiq(
        host=envs.REDIS_HOST,
        port=envs.REDIS_PORT,
        db=envs.REDIS_DB,
        password=envs.REDIS_PASSWORD,
    )
