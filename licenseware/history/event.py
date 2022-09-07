import uuid

from licenseware.history.func import get_value_from_func


def get_event_id(func, func_args, func_kwargs):

    if func.__name__ == "validate_filenames":
        return str(uuid.uuid4())

    if func.__name__ == "upload_files":
        return func_args[1].args.get("event_id") or str(uuid.uuid4())

    event_id = get_value_from_func(func, func_args, func_kwargs, "event_id")

    return event_id
