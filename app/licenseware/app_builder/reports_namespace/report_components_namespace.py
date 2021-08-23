from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.report_components.build_match_expression import build_match_expression



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
                    tenant_id = request.headers.get('Tenantid')
                    filters = build_match_expression(request.json) if request.json else None
                    return component.get_component_data(tenant_id=tenant_id, filters=filters)
            
    return ns
        
       
       
       