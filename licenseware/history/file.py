from licenseware.history.func import get_value_from_func


def get_filepath(func, func_args, func_kwargs):
    filepath = get_value_from_func(func, func_args, func_kwargs, "filepath")
    return filepath
