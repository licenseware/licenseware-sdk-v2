from typing import List

from flask_restx import Namespace, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import machine_check
from licenseware.report_builder import ReportBuilder


def create_report_resource(report: ReportBuilder):
    class ReportRegister(Resource):
        @failsafe(fail_code=500)
        @machine_check
        def get(self):
            return report.register_report()

    return ReportRegister


def get_report_register_namespace(ns: Namespace, reports: List[ReportBuilder]):
    for report in reports:
        RR = create_report_resource(report)

        @ns.doc(
            description="Register report",
            responses={
                200: "Report registered successfully",
                403: "Missing `Authorization` information",
                500: "Could not register report",
            },
        )
        class TempReportResource(RR):
            ...

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + "register",
            (TempReportResource,),
            {},
        )

        ns.add_resource(ReportResource, report.register_report_path)

    return ns
