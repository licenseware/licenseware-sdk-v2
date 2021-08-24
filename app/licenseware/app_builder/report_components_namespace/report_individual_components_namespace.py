from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe



def get_report_individual_components_namespace(ns: Namespace, report_components:list):
    
    for comp in report_components:
            
        @ns.route(comp.component_path)
        class ReportComponent(Resource):
            
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id="Get component data with an optional filter payload",
                responses={
                    200 : 'Success',
                    403 : "Missing `Tenantid` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            def post(self):
                return comp.get_data(request)
        
    return ns
        
       
       
       