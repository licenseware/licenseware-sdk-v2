from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe

from licenseware.report_builder import ReportBuilder
from typing import List



def create_report_resource(report: ReportBuilder):
    
    class ReportController(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return report.return_json_payload()
        
    return ReportController
    


def get_report_metadata_namespace(ns: Namespace, reports:List[ReportBuilder]):
    
    for report in reports:
        
        RR = create_report_resource(report)
        
        @ns.doc(
            id="Get components metadata",
            responses={
                200 : 'Success',
                403 : "Missing `Tenantid` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        class TempReportResource(RR): ...
        
        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + 'metadata',
            (TempReportResource, ),
            {}
        )
        
        ns.add_resource(ReportResource, report.report_path) 
                
    return ns



        
            
