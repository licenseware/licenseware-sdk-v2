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
                    A GET request with no parameters will return a list of available snapshot versions.

                """,
                'params': {
                    'version': {'description': 'Return report snapshot metadata for this version'},
                    "report_id": {"description": "The number of minutes when `public_token` will expire"},
                    'component_id': {'description': 'If `true` will get the read-only url of current generated report. You can later call full report on `report_id`/snapshot'},
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
