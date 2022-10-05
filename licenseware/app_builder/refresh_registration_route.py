"""

When this endpoint is called the registration information from all `App` entities (uploaders, reports etc) are sent to registry service.

"""

from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import machine_check


def add_refresh_registration_route(api: Api, app: type):
    @api.route(app.refresh_registration_path)
    class RefreshRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            description="Register all reports and uploaders",
            responses={
                200: "Registering process was successful",
                403: "Missing `Authorization` information",
                500: "Registering process was unsuccessful",
            },
        )
        def get(self):

            if not app.registrable:
                return {
                    "status": "success",
                    "message": "This app doesn't need registration",
                }, 200

            status_code = 200
            response = app.register_app()

            return response, status_code

    return api
