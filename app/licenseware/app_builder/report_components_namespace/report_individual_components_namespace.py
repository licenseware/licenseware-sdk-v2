from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from marshmallow import Schema, fields
from app.licenseware.utils.miscellaneous import build_restx_model


class ComponentFilterSchema(Schema):
    field_name   = fields.String(required=True)
    filter_type  =  fields.String(required=True)
    filter_value = fields.List(fields.String, required=False)


def get_report_individual_components_namespace(ns: Namespace, report_components:list):
    
    restx_model = build_restx_model(ns, ComponentFilterSchema)

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
                body=restx_model
            )
            def post(self):
                return comp.get_data(request)
        
    return ns
        
       
       
       