"""

Notice we are using `build_restx_model` function to generate the swagger body required for the request. 
Notice also the separation of creating the resource and the given namespace. 

"""

from typing import List

from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.feature_builder import FeatureBuilder


def create_feature_resource(feature: FeatureBuilder):
    class Feature(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return feature.get_status(request)

        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return feature.update_status(request)

    return Feature


def get_features_namespace(ns: Namespace, features: List[FeatureBuilder]):

    update_feature_status_model = ns.model(
        "update_feature_status", dict(activated=fields.Boolean(required=True))
    )

    docs = {
        "get": {
            "description": "Get feature details",
            "responses": {
                200: """\
Example response: 

    {
        "name": "Product Requests",
        "tenant_id": "0be6c669-ab99-41e9-9d88-753a8fcc4cf8",
        "access_levels": [
            "admin"
        ],
        "activated": true,
        "app_id": "plugins",
        "description": "Allow users request products by sending emails",
        "feature_id": "product_requests_feature",
        "monthly_quota": 10,
        "monthly_quota_consumed": 2,
        "quota_reset_date": "2022-03-16T08:18:20.713437"
    }

""",
                403: "Missing `Tenantid` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        },
        "post": {
            "description": "Set feature status",
            "validate": True,
            "expect": [update_feature_status_model],
            "responses": {
                200: "Feature activated/deactivated",
                403: "Missing `Tenantid` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        },
    }

    for feature in features:
        FeatureRes = create_feature_resource(feature)

        FeatureRes.__apidoc__ = docs

        FeatureResource = type(
            feature.feature_id.replace("_", "").capitalize() + "Feature",
            (FeatureRes,),
            {},
        )

        ns.add_resource(FeatureResource, feature.feature_path)

    return ns
