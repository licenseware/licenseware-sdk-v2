"""

When this endpoint is called the generated metadata from marshmallow schemas provided in `AppBuilder` at `editable_tables_schemas` parameter will be returned.

See `editable_table` package for more information.

"""

from flask_restx import Api, Resource

from licenseware.decorators import failsafe


def add_health_route(api: Api, appvars: dict):
    @api.route(appvars["health_path"])
    class HealthRoute(Resource):
        @failsafe(fail_code=500)
        @api.doc(description="Yep still up")
        def get(self):
            return {"status": "success"}

    return api
