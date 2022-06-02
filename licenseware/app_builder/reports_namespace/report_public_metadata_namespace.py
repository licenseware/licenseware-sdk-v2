from typing import List
from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import public_token_check
from licenseware.decorators import failsafe

from licenseware.report_builder import ReportBuilder


def create_report_resource(report: ReportBuilder):

    class ReportController(Resource):
        @failsafe(fail_code=500)
        @public_token_check
        def get(self):
            return report.return_json_payload()

    return ReportController


def get_report_metadata_namespace(ns: Namespace, reports: List[ReportBuilder]):

    for report in reports:

        RR = create_report_resource(report)
        
        # Each table component must have limit/skip to avoid mongo document to large error
        params = {}
        for comp in report.components:
            if comp.component_type != "table": continue
            params[comp.component_id + "_limit"] = {'description': 'Limit the number of results'}
            params[comp.component_id + "_skip"] = {'description': 'Skip the first n results'}
            
        docs = {
            'get': {
                'description': 'Get report metadata',
                'params': {
                    **params,
                    "public_token": {"description": "The token which will be used to return data"}
                },
                'responses': {
                    200: 'Success',
                    403: 'Missing `Tenantid` or `Authorization` information',
                    500: 'Something went wrong while handling the request'
                }
            }
        }

        RR.__apidoc__ = docs

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + 'public_metadata',
            (RR,),
            {}
        )

        ns.add_resource(ReportResource, report.report_path + "/public")


    return ns
