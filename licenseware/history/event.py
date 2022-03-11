import uuid
import inspect


def get_event_id_from_args(func_args):
    for arg in func_args:
        if hasattr(arg, 'headers'):  # flask request
            try:
                return func_args[0].headers.get("EventId")
            except:
                pass
    return None


def get_event_id_from_kwargs(func_kwargs):
    if 'event_id' in func_kwargs:
        return func_kwargs['event_id']
    elif 'flask_request' in func_kwargs:
        return func_kwargs['flask_request'].headers.get("EventId")
    return None


def get_event_id_from_defaults(func):
    return inspect.signature(func).parameters['event_id'].default


def get_event_id(func, func_args, func_kwargs):

    if func.__name__ == 'validate_filenames':
        return str(uuid.uuid4())

    event_id = get_event_id_from_args(func_args)

    if event_id is None:
        event_id = get_event_id_from_kwargs(func_kwargs)
    if event_id is None:
        event_id = get_event_id_from_defaults(func)

    return event_id
