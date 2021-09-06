from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from marshmallow import Schema, fields
from licenseware.utils.miscellaneous import build_restx_model


class ComponentFilterSchema(Schema):
    field_name   = fields.String(required=True)
    filter_type  =  fields.String(required=True)
    filter_value = fields.List(fields.String, required=False)


def get_report_components_namespace(ns: Namespace, reports:list):
    
    restx_model = build_restx_model(ns, ComponentFilterSchema)
    
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
                    body=restx_model
                )
                def post(self):
                    return component.get_data(request)
            
    return ns
        
       
       
       