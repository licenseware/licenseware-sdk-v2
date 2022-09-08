import inspect

from licenseware.common.constants import envs
from licenseware.history import event, file, tenant, uploader


def create_metadata(
    step: str,
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    filepath: str,
    func_name: str = None,
    func_source: str = None,
):
    metadata = {
        "callable": func_name,
        "step": step,
        "source": func_source,
        "tenant_id": tenant_id,
        "event_id": event_id,
        "app_id": envs.APP_ID,
        "uploader_id": uploader_id,
        "filepath": filepath,
    }
    if isinstance(metadata["filepath"], str):
        metadata["file_name"] = metadata["filepath"].split("/")[-1]
    else:
        metadata["file_name"] = ""
    return metadata


def get_metadata(func, func_args, func_kwargs):
    """Getting all the data needed to identify and track files uploaded (function name, source and tenant_id)"""

    metadata = {
        "callable": func.__name__,
        "step": func.__doc__.strip() if func.__doc__ else func.__name__,
        "source": str(inspect.getmodule(func))
        .split("from")[1]
        .strip()
        .replace("'", "")
        .replace(">", ""),
        "tenant_id": tenant.get_tenant_id(func, func_args, func_kwargs)
        if not envs.DESKTOP_ENVIRONMENT
        else envs.DESKTOP_TENANT_ID,
        "event_id": event.get_event_id(func, func_args, func_kwargs),
        "app_id": envs.APP_ID,
        "uploader_id": uploader.get_uploader_id(func, func_args, func_kwargs),
        "filepath": file.get_filepath(func, func_args, func_kwargs),
    }

    # log.info(f"History output metadata {metadata}")

    if metadata["tenant_id"] is None:
        raise Exception(
            f"No `tenant_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')"
        )

    if metadata["event_id"] is None:
        raise Exception(
            f"No `event_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')"
        )

    if metadata["uploader_id"] is None:
        raise Exception(
            f"No `uploader_id` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')"
        )

    # File path must be provided on processing functions
    if metadata["filepath"] is None:
        if func.__name__ not in ["validate_filenames", "upload_files"]:
            raise Exception(
                f"No `filepath` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')"
            )

    if isinstance(metadata["filepath"], str):
        metadata["file_name"] = metadata["filepath"].split("/")[-1]

    return metadata


def add_event_id_to_payload(metadata, response):
    """If history decorator is added on the validation functions from sdk append event_id to payload"""
    if metadata["callable"] in ["validate_filenames", "upload_files"]:
        if isinstance(response, tuple):
            if len(response) == 2:
                return {**response[0], **{"event_id": metadata["event_id"]}}, response[
                    1
                ]
    return response
