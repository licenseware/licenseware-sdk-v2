"""

Small 1 liners utilities that are to small to pe placed in a module 

"""

import os
import random
import string
from typing import List

from flask import Request
from marshmallow import Schema
from marshmallow_jsonschema import JSONSchema

from licenseware.utils.logger import log


def get_flask_request_dict(flask_request: Request):
    from licenseware.common.constants import envs

    """Convert flask request object into a dict"""
    flask_headers = dict(flask_request.headers) if flask_request.headers else {}

    flask_json = {}
    if flask_request.json is not None:
        flask_json = {"flask_request_json": flask_request.json}

    flask_args = dict(flask_request.args) if flask_request.args else {}

    data = {**flask_json, **flask_headers, **flask_args}

    if envs.DESKTOP_ENVIRONMENT and data.get("tenant_id", None) is None:
        for tid in ["tenant_id", "TenantId", "Tenantid"]:
            data[tid] = envs.DESKTOP_TENANT_ID
        data["Authorization"] = "Authorization not needed on desktop"

    return data


def serialize_flask_request(flask_request: Request):
    log.warning(
        "Please use `get_flask_request_dict` instead. This was a bad naming function, will be removed"
    )
    return get_flask_request_dict(flask_request)


def set_environment_variables(*, envs: dict = None, env_path: str = ".env"):
    """

    In the case we need to set some environment variables
    either providing a dict or loading from .env file this function may come in handy

    Make sure to call the `set_environment_variables` before the envs are needed!

    ```py

        from licenseware.utils.miscellaneous import set_environment_variables
        set_environment_variables()


        App = AppBuilder(
            name = 'App Name',
            description = 'App long description',
            flags = [flags.BETA]
        )

    ```

    """

    if os.getenv("ENVIRONMENT") not in ["local", None]:
        return

    if envs:
        os.environ.update(envs)
        return

    with open(env_path, "r") as f:
        env_vars = {}
        for v in f.readlines():
            vli = v.strip().split("=")
            if len(vli) == 2:
                env_vars[vli[0]] = vli[1]
            else:
                env_vars[vli[0]] = ""

        os.environ.update(env_vars)


def generate_id(length=6):
    """Create a random series of digits of length specified"""
    return "".join([random.choice(list(string.digits)) for _ in range(length)])


def flat_dict(li: List[dict]) -> dict:
    """
    - input_list = [{'width': 'full'}, {'height': '100vh'}]
    - output_dict = {'width': 'full', 'height': '100vh'}
    """
    return {k: v for dict_ in li for k, v in dict_.items()}


def get_json_schema(schema: Schema):
    """
    Generate json schema from marshmallow schema class
    """

    json_schema = JSONSchema().dump(schema())["definitions"][schema.__name__]

    return json_schema


def build_restx_model(ns, schema: Schema, model_name: str = None):
    """
    !DEPRECIATED - use `marshmallow_to_restx_model`function instead

    Convert a marshmallow schema to a flask restx model
    Resulted restx model can be used for swagger (body, marshal_with, expect, etc)
    """

    model_name = model_name or schema.__name__

    json_schema = get_json_schema(schema)
    restx_model = ns.schema_model(model_name, json_schema)

    return restx_model


http_methods = ["GET", "POST", "PUT", "DELETE"]

swagger_authorization_header = {
    "Tenantid": {"type": "apiKey", "in": "header", "name": "Tenantid"},
    "Authorization": {"type": "apiKey", "in": "header", "name": "Authorization"},
}
