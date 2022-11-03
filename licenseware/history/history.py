import time
import traceback
from functools import wraps
from typing import Callable

from licenseware.pubsub.producer import Producer
from licenseware.pubsub.types import TopicType, EventType
from licenseware.utils.logger import log as logg
from .metadata import get_metadata
from .schemas import HistorySchema, Status
from .utils import get_kafka_producer


def log_file_validation(
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    file_validation: list,
    filepaths: list,
    producer: Producer,
):
    pass


def get_processing_time(start_time: float):
    if start_time is None:
        return
    total_seconds = time.perf_counter() - start_time
    processing_time = time.strftime("%M:%S", time.gmtime(total_seconds))
    return processing_time


def log_processing_success(
    producer: Producer,
    metadata: HistorySchema,
    start_time: float = None,
):
    metadata.processing_time = get_processing_time(start_time)
    metadata.status = Status.SUCCESS
    metadata.event_type = EventType.PROCESSING_DETAILS
    producer.publish(TopicType.LOG_EVENTS, metadata.dict())
    return metadata


def log_processing_failure(
    producer: Producer,
    metadata: HistorySchema,
    start_time: float = None,
    error: str = None,
    traceback: str = None,
):
    metadata.processing_time = get_processing_time(start_time)
    metadata.error = error
    metadata.traceback = traceback
    metadata.status = Status.FAILED
    metadata.event_type = EventType.PROCESSING_DETAILS
    logg.debug(metadata.dict())
    producer.publish(TopicType.LOG_EVENTS, metadata.dict())
    return metadata


def log(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        meta = get_metadata(f, args, kwargs)
        producer = get_kafka_producer(f, args, kwargs)
        start_time = time.perf_counter()

        try:
            response = f(*args, **kwargs)
            if producer is None:
                return response

            log_processing_success(producer, meta, start_time)

            return response
        except Exception as err:
            logg.error(err)
            if producer is None:
                raise err

            log_processing_failure(
                producer,
                meta,
                start_time,
                error=str(err),
                traceback=str(traceback.format_exc()),
            )

            return f(*args, **kwargs)

    return wrapper
