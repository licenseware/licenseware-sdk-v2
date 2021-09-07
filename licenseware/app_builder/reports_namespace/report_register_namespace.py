from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import machine_check
from licenseware.decorators import failsafe



def get_report_register_namespace(ns: Namespace, reports:list):
    
    for report in reports:
    
        @ns.route(report.register_report_path)
        class ReportRegister(Resource):         
            @failsafe(fail_code=500)   
            @machine_check
            @ns.doc(
                id=f"Register {report.name} report",
                responses={
                    200 : "Report registered successfully",
                    403 : "Missing `Authorization` information",
                    500 : "Could not register report" 
                },
            )
            def get(self):
                return report.register_report()
            
    return ns
        
             