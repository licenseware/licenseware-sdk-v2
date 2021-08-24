from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe



def get_report_components_namespace(ns: Namespace, reports:list):
    
    for report in reports:
        for component in report.components:
            
            @ns.route(report.report_path + component.path)
            class BaseResourcePost(Resource):
                
                @failsafe(fail_code=500)
                @authorization_check
                @ns.doc(
                    id="Get components data with an optional filter payload",
                    responses={
                        200 : 'Success',
                        403 : "Missing `Tenantid` or `Authorization` information",
                        500 : 'Something went wrong while handling the request' 
                    },
                )
                def post(self):
                    return component.get_data(request)
            
    return ns
        
       
       
       