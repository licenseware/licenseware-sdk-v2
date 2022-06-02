from typing import List
from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe

from licenseware.report_builder import ReportBuilder
from licenseware.download import download_all


def create_report_resource(report: ReportBuilder):

    class ReportController(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):

            file_type = request.args.get('download_as')
            latest = request.args.get('latest', 'false') 
            snapshot = request.args.get('snapshot', 'false') 
            tenant_id = request.headers.get('Tenantid')

            if latest == "true": 
                return report.get_report_snapshot(request)

            if snapshot == "true": 
                return report.get_readonly_report_url(request)

            if file_type is None:
                return report.return_json_payload()
            else:
                return download_all(
                    file_type,
                    report,
                    tenant_id,
                    filename=report.report_id + '.' + file_type,
                    flask_request=request
                )

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
                    'latest': {'description': 'If `true` will get the report in one call. Make sure to add limit and skip.'},
                    'snapshot': {'description': 'If `true` will get the read-only url of current generated report.'},
                    'download_as': {'description': 'Download table component as file type: csv, xlsx, json'}
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
            report.report_id.replace("_", "").capitalize() + 'metadata',
            (RR,),
            {}
        )

        ns.add_resource(ReportResource, report.report_path)


    return ns
