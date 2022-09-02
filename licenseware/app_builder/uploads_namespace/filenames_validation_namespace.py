"""

Given a list of filenames return validation analysis response

Notice we are using `build_restx_model` function to generate the swagger body required for the request. 

Notice also the separation of creating the resource and the given namespace. 

"""


from typing import List

from flask import request
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware.common import marshmallow_to_restx_model
from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.uploader_builder import UploaderBuilder


class FilenamesValidationSchema(Schema):
    filenames = fields.List(fields.Str, required=True)


class FilenamesRespValidationSchema(Schema):
    status = fields.Str()
    filename = fields.Str()
    message = fields.Str()


class FilenamesRespSchema(Schema):
    status = fields.Str(metadata=dict(description="Statuses: `success` or `failed`"))
    message = fields.Str()
    validation = fields.List(fields.Nested(FilenamesRespValidationSchema))
    event_id = fields.Str(
        metadata=dict(
            description="The `event_id` which needs to be returned as a query param when uploading these files"
        )
    )


def create_uploader_resource(uploader: UploaderBuilder):
    class FilenameValidate(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return uploader.validate_filenames(request)

    return FilenameValidate


def get_filenames_validation_namespace(ns: Namespace, uploaders: List[UploaderBuilder]):

    filenames_model = marshmallow_to_restx_model(ns, FilenamesValidationSchema)
    filenames_resp_model = marshmallow_to_restx_model(ns, FilenamesRespSchema)

    for uploader in uploaders:

        if uploader.validator_class is None:
            continue

        UR = create_uploader_resource(uploader)

        @ns.doc(
            description="Validating the list of filenames provided",
            responses={
                402: "Quota exceeded",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        @ns.expect(filenames_model)
        @ns.response(
            code=200,
            description="Filenames validation response",
            model=filenames_resp_model,
        )
        class TempUploaderResource(UR):
            ...

        # Adding extra swagger query parameters if provided
        if uploader.query_params_on_validation:

            params_dict = {}
            for (
                param_name,
                param_description,
            ) in uploader.query_params_on_validation.items():
                params_dict[param_name] = {"description": param_description}

            TempUploaderResource.__apidoc__.update({"params": params_dict})

        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + "filenames",
            (TempUploaderResource,),
            {},
        )

        ns.add_resource(UploaderResource, uploader.upload_validation_path)

    return ns
