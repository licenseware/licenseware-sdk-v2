import uuid
from .func import get_value_from_func


def get_event_id(func, func_args, func_kwargs):

    if func.__name__ == 'validate_filenames':
        return str(uuid.uuid4())

    event_id = get_value_from_func(func, func_args, func_kwargs, "event_id", "EventId")

    if event_id is None and func.__name__ == 'upload_files':
        return str(uuid.uuid4())

    return event_id
