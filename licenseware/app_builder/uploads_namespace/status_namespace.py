from typing import List

from flask import request
from flask_restx import Namespace, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check

# from licenseware.tenants.processing_status import get_uploader_status #! OUTDATED
from licenseware.notifications.uploader_status import get_uploader_status
from licenseware.uploader_builder import UploaderBuilder


def create_uploader_resource(uploader: UploaderBuilder):
    class UploaderStatus(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return get_uploader_status(
                request.headers.get("Tenantid"), uploader.uploader_id
            )
            # return get_uploader_status(request.headers.get("Tenantid"), uploader.uploader_id)

    return UploaderStatus


def get_status_namespace(ns: Namespace, uploaders: List[UploaderBuilder]):

    for uploader in uploaders:

        UR = create_uploader_resource(uploader)

        @ns.doc(
            description="Get processing status of files uploaded",
            responses={
                200: "idle or running",
                400: "Tenantid not provided",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        class TempUploaderResource(UR):
            ...

        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + "status",
            (TempUploaderResource,),
            {},
        )

        ns.add_resource(UploaderResource, uploader.status_check_path)

    return ns
