import inspect
from licenseware.constants.worker_event_type import WorkerEvent


def get_value_from_kwargs(func_kwargs, *params):

    for param in params:
        if func_kwargs.get(param) is not None:
            return func_kwargs[param]

    if func_kwargs.get("event") is not None:

        if isinstance(func_kwargs["event"], dict):
            for param in params:
                value = func_kwargs["event"].get(param)
                if value is not None:
                    return value

        if isinstance(func_kwargs["event"], WorkerEvent):
            for param in params:
                if not hasattr(func_kwargs["event"], param):
                    continue
                value = getattr(func_kwargs["event"], param)
                if value is not None:
                    return value
    return None


def get_value_from_defaults(func, *params):
    for param in params:
        try:
            value = inspect.signature(func).parameters[param].default
            if value is not None:
                return value
        except:
            pass


def get_value_from_self(func_args, *params):

    if len(func_args) == 0:
        return

    for param in params:
        if not hasattr(func_args[0], param):
            continue
        value = getattr(func_args[0], param)
        if value is not None:
            return value

    if hasattr(func_args[0], "event"):
        if not isinstance(func_args[0].event, WorkerEvent):
            return
        for param in params:
            if not hasattr(func_args[0].event, param):
                continue
            value = getattr(func_args[0].event, param)
            if value is not None:
                return value


def get_value_from_func(func, func_args, func_kwargs, *params):
    """Get parameters value from function data"""

    value = get_value_from_kwargs(func_kwargs, *params)

    if value is None:
        value = get_value_from_defaults(func, *params)
    if value is None:
        value = get_value_from_self(func_args, *params)

    return value
