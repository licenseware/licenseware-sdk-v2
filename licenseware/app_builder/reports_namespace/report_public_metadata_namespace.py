from typing import List

from flask_restx import Namespace, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import public_token_check
from licenseware.report_builder import ReportBuilder


def create_report_resource(report: ReportBuilder):
    class ReportController(Resource):
        @failsafe(fail_code=500)
        @public_token_check
        def get(self):
            return report.return_json_payload()

    return ReportController


def get_public_report_metadata_namespace(ns: Namespace, reports: List[ReportBuilder]):

    for report in reports:

        RR = create_report_resource(report)

        docs = {
            "get": {
                "description": "Get public report metadata",
                "params": {
                    "public_token": {
                        "description": "The token which will be used to return data"
                    }
                },
                "responses": {
                    200: "Success",
                    403: "Public token missing or invalid",
                    500: "Something went wrong while handling the request",
                },
            }
        }

        RR.__apidoc__ = docs

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + "public_metadata",
            (RR,),
            {},
        )

        ns.add_resource(ReportResource, report.report_path + "/public")

    return ns
