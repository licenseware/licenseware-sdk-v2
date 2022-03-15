from .func import get_value_from_func


def get_uploader_id(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "X-Forwarded-Path", "UploaderId", "uploader_id")
    if value is None: return
    if isinstance(value, str):
        if '/uploads' in value and value.endswith(('/validation', '/files', )):  # url
            # ex: 'universal-uploader/uploads/universal_uploader/validation' where app_id/uploads/uploader_id
            url_list = value.split('/')
            uploader_id = url_list[url_list.index('uploads') + 1]
            return uploader_id
    else:
        return value
