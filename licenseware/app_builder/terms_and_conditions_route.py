import importlib.resources as pkg_resources
import os
import sys

from flask_restx import Api, Resource

from licenseware import resources
from licenseware.decorators import failsafe


def add_terms_and_conditions_route(api: Api, appvars: dict):

    resources_path = os.path.join(
        sys.path[0], "app/resources/terms_and_conditions.html"
    )

    if os.path.exists(resources_path):
        with open(resources_path) as f:
            raw_html = f.read()
    else:
        raw_html = pkg_resources.read_text(resources, "terms_and_conditions.html")

    @api.route(appvars["terms_and_conditions_path"])
    class TermsAndConds(Resource):
        @failsafe(fail_code=500)
        @api.doc(
            description="Return terms and conditions html page",
            responses={
                200: "Terms and Conditions raw html data",
                500: "Something went wrong while handling the request",
            },
        )
        def get(self):
            return raw_html

    return api
