import inspect


def get_value_from_args(func_args, *params):
    for arg in func_args:
        if hasattr(arg, 'headers'):  # flask request
            try:
                for param in params:
                    value = arg.headers.get(param)
                    if value: return value
            except:
                pass
    return None


def get_value_from_kwargs(func_kwargs, *params):
    for param in params:
        if func_kwargs.get(param) is not None:
            return func_kwargs[param]

    if func_kwargs.get('flask_request') is not None:
        try:
            for param in params:
                if isinstance(func_kwargs['flask_request'], dict):
                    value = func_kwargs['flask_request'].get(param)
                else:
                    value = func_kwargs['flask_request'].headers.get(param)
                if value: return value
        except:
            pass

    if func_kwargs.get('event') is not None:
        if isinstance(func_kwargs['event'], dict):
            for param in params:
                value = func_kwargs['event'].get(param)
                if value: return value

    return None


def get_value_from_defaults(func, *params):
    for param in params:
        try:
            value = inspect.signature(func).parameters[param].default
            if value: return value
        except: pass


def get_value_from_func(func, func_args, func_kwargs, *params):
    """ Get parameters value from function data """

    value = get_value_from_args(func_args, *params)

    if value is None:
        value = get_value_from_kwargs(func_kwargs, *params)
    if value is None:
        value = get_value_from_defaults(func, *params)

    return value
