from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe



def get_report_metadata_namespace(ns: Namespace, reports:list):
    
    for report in reports:
        
        @ns.route(report.report_path)
        class ReportController(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id="Get components metadata",
                responses={
                    200 : 'Success',
                    403 : "Missing `Tenantid` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            def get(self):
                return report.return_json_payload()
            
    return ns
        
            
