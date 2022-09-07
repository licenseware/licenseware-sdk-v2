from licenseware.history.func import get_value_from_func


def get_uploader_id(func, func_args, func_kwargs):
    value = get_value_from_func(
        func, func_args, func_kwargs, "uploader_id", "UploaderId"
    )
    return value
