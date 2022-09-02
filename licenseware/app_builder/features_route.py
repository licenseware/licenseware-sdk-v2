"""

When this endpoint is called the generated metadata from marshmallow schemas provided in `AppBuilder` at `editable_tables_schemas` parameter will be returned.

See `editable_table` package for more information.

"""

from flask import request
from flask_restx import Api, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.feature_builder.utils import get_all_features


def add_features_route(api: Api, appvars: dict):
    @api.route(appvars["features_path"])
    class AllFeatures(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Get all available features(add-ons) for this app",
            responses={
                200: """\

Example response:

    {
        "available_features": [
            {
            "app_id": "plugins",
            "name": "Product Requests",
            "description": "Allow users request products by sending emails",
            "access_levels": [
                "admin"
            ],
            "monthly_quota": 10,
            "activated": false,
            "feature_id": "product_requests_feature",
            "feature_path": "/product-requests"
            }
        ],
        "initialized_features": [
            {
            "name": "Product Requests",
            "tenant_id": "0be6c669-ab99-41e9-9d88-753a8fcc4cf8",
            "access_levels": [
                "admin"
            ],
            "app_id": "plugins",
            "description": "Allow users request products by sending emails",
            "feature_id": "product_requests_feature",
            "feature_path": "/product-requests",
            "monthly_quota": 10
            }
        ]
    }

""",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        def get(self):
            return {
                "available_features": [f.get_details() for f in appvars["features"]],
                "initialized_features": get_all_features(request),
            }

    return api
