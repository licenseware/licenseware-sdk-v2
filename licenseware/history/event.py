import uuid
from .func import get_value_from_func


def get_event_id(func, func_args, func_kwargs):

    if func.__name__ == 'validate_filenames':
        return str(uuid.uuid4())

    return get_value_from_func(func, func_args, func_kwargs, "event_id", "EventId")
