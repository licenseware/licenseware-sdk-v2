from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.decorators import failsafe



def get_report_register_namespace(ns: Namespace, reports:list):
    
    for report in reports:
    
        @ns.route(report.register_report_path)
        class ReportRegister(Resource):         
            @failsafe(fail_code=500)   
            @machine_check
            @ns.doc(
                id=f"Register {report.name} report",
                responses={
                    200 : 'Report registered',
                    403 : "Missing `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            def get(self):
                return report.register_report()
            
    return ns
        
             
