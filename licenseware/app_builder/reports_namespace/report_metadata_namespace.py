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
            latest = request.args.get('latest') # TODO remove when report_snapshot ready
            tenant_id = request.headers.get('Tenantid')

            if latest is not None: # TODO remove when report_snapshot ready
                return report.get_report_snapshot(request)

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

        @ns.doc(
            description="Get report metadata",
            responses={
                200: 'Success',
                403: "Missing `Tenantid` or `Authorization` information",
                500: 'Something went wrong while handling the request'
            },
        )
        @ns.param(name="download_as", description="Download all report components in csv, xlsx or pdf format.")
        @ns.param(name="latest", description="Get latest saved report") # TODO remove when report_snapshot ready
        class TempReportResource(RR): ...

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + 'metadata',
            (TempReportResource,),
            {}
        )

        ns.add_resource(ReportResource, report.report_path)

    return ns
