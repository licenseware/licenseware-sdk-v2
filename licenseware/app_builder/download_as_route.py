from flask import request
from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.download import download_as


def add_download_as_route(api: Api, appvars: dict):

    resource_fields = api.model("DataList", {})

    @api.route("/download/<string:file_type>")
    class DownloadAs(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Given json data will return file of type: json, csv or xlsx",
            responses={
                200: "Downloaded file (`file_type` can be: json, csv, xlsx)",
                400: "File type not supported",
                500: "Something went wrong while handling the request",
            },
        )
        @api.expect([resource_fields])
        def post(self, file_type):

            tenant_id = request.headers.get("Tenantid")
            data = request.json

            return download_as(file_type, data, tenant_id)

    return api
