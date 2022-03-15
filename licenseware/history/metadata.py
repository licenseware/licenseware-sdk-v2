import inspect
from licenseware.common.constants import envs

from . import event, tenant, uploader, file


def create_metadata(
        step: str,
        tenant_id: str,
        event_id: str,
        uploader_id: str,
        filepath: str,
        func_name: str = None,
        func_source: str = None,
):
    return {
        'callable': func_name,
        'step': step,
        'source': func_source,
        'tenant_id': tenant_id,
        'event_id': event_id,
        'app_id': envs.APP_ID,
        'uploader_id': uploader_id,
        'filepath': filepath
    }


def get_metadata(func, func_args, func_kwargs):
    """ Getting all the data needed to identify and track files uploaded (function name, source and tenant_id) """

    print("History inputs:", func.__name__, func_args, func_kwargs)

    metadata = {
        'callable': func.__name__,
        'step': func.__doc__.strip() if func.__doc__ else func.__name__,
        'source': str(inspect.getmodule(func)).split("from")[1].strip().replace("'", "").replace(">", ""),
        'tenant_id': tenant.get_tenant_id(func, func_args, func_kwargs),
        'event_id': event.get_event_id(func, func_args, func_kwargs),
        'app_id': envs.APP_ID,
        'uploader_id': uploader.get_uploader_id(func, func_args, func_kwargs),
        'filepath': file.get_filepath(func, func_args, func_kwargs)
    }

    print("History output metadata:", metadata)

    if metadata['tenant_id'] is None:
        raise Exception(
            f"No `tenant_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')")

    if metadata['event_id'] is None:
        raise Exception(
            f"No `event_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')")

    if metadata['uploader_id'] is None:
        raise Exception(
            f"No `uploader_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')")

    # File path must be provided on processing functions
    if metadata['filepath'] is None:
        if func.__name__ not in ['validate_filenames', 'upload_files']:
            raise Exception(
                f"No `filepath` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')")

    return metadata


def append_headers_on_validation_funcs(metadata, response):
    """ If history decorator is added on the  validation functions from sdk append EventId and UploaderId headers """
    if metadata['callable'] in ['validate_filenames', 'upload_files']:
        if isinstance(response, tuple):
            if len(response) == 2:  # if returns something like: {"status": "success", "message": "ok"}, 200
                return *response, {"EventId": metadata['event_id'], "UploaderId": metadata['uploader_id']}
    return response
