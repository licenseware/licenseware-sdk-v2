import inspect
import json
import os

from .func import get_value_from_func
from licenseware.utils.alter_string import get_altered_strings


def get_entities(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "entities")
    return value


def get_event_type(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "event_type")
    return value


def get_app_name(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "app_name")
    if value:
        return value
    value = get_value_from_func(func, func_args, func_kwargs, "app_id")
    return get_altered_strings(value).title


def get_uploader_name(func, func_args, func_kwargs):
    value = get_value_from_func(func, func_args, func_kwargs, "uploader_name")
    if value:
        return value
    value = get_value_from_func(func, func_args, func_kwargs, "uploader_id")
    return get_altered_strings(value).title


def get_uploader_id(func, func_args, func_kwargs):
    value = get_value_from_func(
        func, func_args, func_kwargs, "uploader_id", "UploaderId"
    )
    return value


def get_tenant_id(func, func_args, func_kwargs):
    return get_value_from_func(func, func_args, func_kwargs, "tenant_id", "TenantId")


def get_app_id(func, func_args, func_kwargs):
    return get_value_from_func(func, func_args, func_kwargs, "app_id")


def get_event_id(func, func_args, func_kwargs):
    event_id = get_value_from_func(func, func_args, func_kwargs, "event_id")
    return event_id


def get_filepath(func, func_args, func_kwargs):
    filepath = get_value_from_func(func, func_args, func_kwargs, "filepath")
    return filepath


def get_filename(func, func_args, func_kwargs):
    filepath = get_value_from_func(func, func_args, func_kwargs, "filepath")
    if filepath is not None:
        return os.path.basename(filepath)
    return None


def get_kafka_producer(func, func_args, func_kwargs):
    kafka_producer = get_value_from_func(
        func, func_args, func_kwargs, "kafka_producer", "producer"
    )
    return kafka_producer


def get_config(func, func_args, func_kwargs):
    config = get_value_from_func(func, func_args, func_kwargs, "config")
    return config


def get_func_source(func):
    source = (
        str(inspect.getmodule(func))
        .split("from")[1]
        .strip()
        .replace("'", "")
        .replace(">", "")
    )
    return f"Method: {str(func).split(' ')[1]} from: {os.path.relpath(source)}"


class ObjectHandler(json.JSONEncoder):
    def default(self, obj):
        return str(obj)


def get_func_doc(func):
    if func.__doc__:
        return func.__doc__.strip()
    return get_altered_strings(func.__name__).title


def get_parsed_func_args(func_args: tuple):

    if func_args is None:
        return

    return json.loads(json.dumps(func_args, cls=ObjectHandler))


def get_parsed_func_kwargs(func_kwargs: dict):

    if func_kwargs is None:
        return

    return json.loads(json.dumps(func_kwargs, cls=ObjectHandler))
