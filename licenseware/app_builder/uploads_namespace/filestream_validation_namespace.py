"""
Here we have the uploader route builder section.
Each time we have a list of entities we need to create a new route or a similar route, like we have below.
We need to separate the resource from the restx namespace, otherwise the resource will be overwrited.

"""


from typing import List

from flask import request
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

from licenseware.common import marshmallow_to_restx_model
from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.tenants import clear_tenant_data
from licenseware.uploader_builder import UploaderBuilder
from licenseware.utils.common import trigger_broker_funcs


class FileUploadDetailedValidationSchema(Schema):
    status = fields.Str()
    message = fields.Str()
    filename = fields.Str()
    filepath = fields.Str()


class FileUploadValidationSchema(Schema):
    tenant_id = fields.Str()
    status = fields.Str()
    message = fields.Str()
    validation = fields.List(fields.Nested(FileUploadDetailedValidationSchema))


class FileUploadEventDataSchema(Schema):
    tenant_id = fields.Str()
    uploader_id = fields.Str()
    event_id = fields.Str()
    filepaths = fields.List(fields.Str)
    flask_request = fields.List(fields.Raw)
    validation_response = fields.Nested(FileUploadValidationSchema)


class FileUploadRespSchema(Schema):
    status = fields.Str()
    message = fields.Str()
    # event_data = fields.List(fields.Nested(FileUploadEventDataSchema))
    event_id = fields.Str()


def create_uploader_resource(uploader: UploaderBuilder):
    class FileStreamValidate(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def post(self):

            clear_data = request.args.get("clear_data", "false")
            if "true" in clear_data.lower():
                clear_tenant_data(
                    request.headers.get("Tenantid"), uploader.collections_list
                )

            upload_response = uploader.upload_files(request)
            if uploader.broker_funcs:
                trigger_broker_funcs(
                    request, uploader.broker_funcs, upload_response=upload_response[0]
                )

            return upload_response

    return FileStreamValidate


def get_filestream_validation_namespace(
    ns: Namespace, uploaders: List[UploaderBuilder]
):

    file_validation_resp_model = marshmallow_to_restx_model(ns, FileUploadRespSchema)

    file_upload_parser = ns.parser()
    file_upload_parser.add_argument(
        "files[]",
        location="files",
        type=FileStorage,
        required=True,
        # action="append", # Uploading multiple files doesn't work on swagger
        help="Upload files for processing",
    )

    default_params = {
        "clear_data": "Boolean parameter, warning, will clear existing data",
        "event_id": "The uuid4 string received on filenames validation",
    }

    for uploader in uploaders:

        if uploader.worker is None:
            continue

        UR = create_uploader_resource(uploader)

        @ns.doc(
            description="Upload files received on `files[]` for processing",
            params=default_params,
            responses={
                400: "File list is empty or files are not on 'files[]' key",
                402: "Quota exceeded",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        @ns.expect(file_upload_parser)
        @ns.response(
            code=200, description="Upload response", model=file_validation_resp_model
        )
        class TempUploaderResource(UR):
            ...

        # Adding extra swagger query parameters if provided
        if uploader.query_params_on_upload:

            if isinstance(uploader.query_params_on_upload, list):
                params_dict = {}
                for param in uploader.query_params_on_upload:
                    params_dict[param["id"]] = {
                        "description": param["description"],
                        "allowed_values": param["allowed_values"],
                    }
            else:
                params_dict = {}
                for (
                    param_name,
                    param_description,
                ) in uploader.query_params_on_upload.items():
                    params_dict[param_name] = {"description": param_description}

            TempUploaderResource.__apidoc__.update(
                {"params": {**default_params, **params_dict}}
            )

        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + "stream",
            (TempUploaderResource,),
            {},
        )

        ns.add_resource(UploaderResource, uploader.upload_path)

    return ns
