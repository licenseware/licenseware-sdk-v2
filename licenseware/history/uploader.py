from .func import get_value_from_func
from licenseware.common.constants import envs


def get_uploader_id(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "X-Forwarded-Path", "UploaderId", "uploader_id")
    if value is None: return
    if f'{envs.APP_ID}/uploads' in value and value.endswith(('/validation', '/files', )):  # url
        # ex: 'universal-uploader/uploads/universal_uploader/validation' where app_id/uploads/uploader_id
        url_list = value.split('/')
        return url_list[url_list.index('uploads') + 1]
    else:
        return value
