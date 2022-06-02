from typing import List
from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators import failsafe
from licenseware.report_builder import ReportBuilder


def create_report_snapshot_resource(report: ReportBuilder):

    class ReportController(Resource):
        @failsafe(fail_code=500)
        def get(self):
            return report.get_readonly_report(request)

    return ReportController


def get_report_snapshot_namespace(ns: Namespace, reports: List[ReportBuilder]):

    for report in reports:

        RR = create_report_snapshot_resource(report)
        
        docs = {
            'get': {
                'description': """
                    Get full report. 
                    For this to be available on get report metadata url, set query param `snapshot` to true.
                    The report will be created and available at this link. 
                """,
                'params': {
                    'tenant_id': {'description': 'The tenant_id which owns the data'},
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
            report.report_id.replace("_", "").capitalize() + 'snapshot',
            (RR,),
            {}
        )

        ns.add_resource(ReportResource, report.report_path + "/snapshot")

    return ns
