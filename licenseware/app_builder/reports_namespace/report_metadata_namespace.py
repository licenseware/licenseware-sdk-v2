from typing import List

from flask import request
from flask_restx import Namespace, Resource

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.download import download_all
from licenseware.report_builder import ReportBuilder


def create_report_resource(report: ReportBuilder):
    class ReportController(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):

            snapshot = request.args.get("snapshot")
            public_url = request.args.get("public_url")
            file_type = request.args.get("download_as")
            tenant_id = request.headers.get("Tenantid")

            if snapshot == "true":
                return report.get_snapshot_version(request)

            if public_url == "true":
                return report.get_report_public_url(request)

            if public_url == "false":
                return report.delete_report_public_url(request)

            if file_type is not None:
                return download_all(
                    file_type,
                    report,
                    tenant_id,
                    filename=report.report_id + "." + file_type,
                    flask_request=request,
                )

            return report.return_json_payload()

    return ReportController


def get_report_metadata_namespace(ns: Namespace, reports: List[ReportBuilder]):

    for report in reports:

        RR = create_report_resource(report)

        docs = {
            "get": {
                "description": "Get report metadata",
                "params": {
                    "public_url": {
                        "description": "If `true` will return the public url for this report. If `false` will delete public url for this report."
                    },
                    "expire": {
                        "description": "The number of minutes when `public_token` will expire"
                    },
                    "snapshot": {
                        "description": "If `true` will get the read-only url of current generated report. You can later call full report on `report_id`/snapshot"
                    },
                    "download_as": {
                        "description": "Download table component as file type: csv, xlsx, json"
                    },
                },
                "responses": {
                    200: "Success",
                    403: "Missing `Tenantid` or `Authorization` information",
                    500: "Something went wrong while handling the request",
                },
            }
        }

        RR.__apidoc__ = docs

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + "metadata", (RR,), {}
        )

        ns.add_resource(ReportResource, report.report_path)

    return ns
