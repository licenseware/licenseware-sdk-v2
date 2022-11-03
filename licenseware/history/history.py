import time
import traceback
from functools import wraps
from typing import Callable, Union, List
from datetime import datetime

from licenseware.constants.worker_event_type import WorkerEvent
from licenseware.pubsub.producer import Producer
from licenseware.pubsub.types import TopicType, EventType
from licenseware.utils.logger import log as logg
from .metadata import get_metadata
from .schemas import HistorySchema, Status, EventTypes
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


def publish(producer: Producer, metadata: Union[dict, HistorySchema], **kwargs):
    if isinstance(metadata, dict):
        metadata = HistorySchema(**metadata)
    metadata.processing_time = get_processing_time(kwargs.get("start_time"))
    metadata.status = metadata.status or kwargs.get("status")
    metadata.event_type = metadata.event_type or kwargs.get("event_type")
    metadata.error = metadata.error or kwargs.get("error")
    metadata.traceback = metadata.traceback or kwargs.get("traceback")
    producer.publish(TopicType.LOG_EVENTS, metadata.dict())
    return metadata


def publish_entities(
    producer: Producer,
    metadata: Union[dict, HistorySchema, WorkerEvent],
    entities: Union[List[str], List[dict]],
):
    if not isinstance(metadata, dict):
        metadata = metadata.dict()
    metadata.pop("event_type", None)
    return publish(
        producer,
        HistorySchema(
            **metadata,
            event_type=EventTypes.ENTITIES_EXTRACTED,
            entities=entities,
            description="Published entities",
            updated_at=datetime.utcnow().isoformat(),
        ),
    )


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

            publish(
                producer,
                meta,
                status=Status.SUCCESS,
                event_type=EventType.PROCESSING_DETAILS,
                start_time=start_time,
            )

            return response
        except Exception as err:
            logg.error(err)
            if producer is None:
                raise err

            publish(
                producer,
                meta,
                status=Status.FAILED,
                event_type=EventType.PROCESSING_DETAILS,
                tart_time=start_time,
                error=str(err),
                traceback=str(traceback.format_exc()),
            )

            return f(*args, **kwargs)

    return wrapper
