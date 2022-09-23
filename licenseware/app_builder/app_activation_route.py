"""

When this endpoint is called the `Quota` for this tenant_id must be created and the `App` must be registered.

"""

from flask import request
from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.registry_service import register_app
from licenseware.uploader_builder import UploaderBuilder


def add_app_activation_route(api: Api, appvars: dict):
    @api.route(appvars["app_activation_path"])
    class InitializeTenantApp(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Initialize app for tenant_id",
            responses={
                200: "Quota is within limits",
                400: "Tenantid not provided",
                402: "Quota exceeded",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        def get(self):

            if not appvars["registrable"]:
                return {
                    "status": "success",
                    "message": "This app doesn't need registration",
                }, 200

            tenant_id = request.headers.get("Tenantid")

            if not tenant_id:
                return {"status": "fail", "message": "Tenantid not provided"}, 403

            for uploader in appvars["uploaders"]:
                uploader: UploaderBuilder

                qmsg, status_code = uploader.init_tenant_quota(
                    tenant_id=tenant_id, auth_token=request.headers.get("Authorization")
                )

                if status_code != 200:
                    return qmsg, status_code

            dmsg, _ = register_app(**appvars)

            if dmsg["status"] != "success":
                return {"status": "fail", "message": "App failed to register"}, 500

            return {"status": "success", "message": "App installed successfully"}, 200

    return api
