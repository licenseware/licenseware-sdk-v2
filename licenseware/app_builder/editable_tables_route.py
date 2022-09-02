"""

When this endpoint is called the generated metadata from marshmallow schemas provided in `AppBuilder` at `editable_tables_schemas` parameter will be returned.

See `editable_table` package for more information.

"""

from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.editable_table import editable_tables_from_schemas


def add_editable_tables_route(api: Api, appvars: dict):
    @api.route(appvars["editable_tables_path"])
    class EditableTables(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Get editable tables metadata",
            responses={
                200: "",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        def get(self):
            return editable_tables_from_schemas(appvars["editable_tables_schemas"])

    return api
