"""

When this endpoint is called the registration information for this `App` is sent to registry-service.

"""

from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import machine_check
from licenseware.registry_service import register_app


def add_app_registration_route(api: Api, appvars: dict):
    @api.route(appvars["register_app_path"])
    class AppRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            description="Register app to registry-service",
            responses={
                200: "Registration successful",
                403: "Missing `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        def get(self):
            if not appvars["registrable"]:
                return {
                    "status": "success",
                    "message": "This app doesn't need registration",
                }, 200
            return register_app(**appvars)

    return api
