from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from marshmallow import Schema, fields
from licenseware.utils.miscellaneous import build_restx_model


from licenseware.report_builder import ReportBuilder
from licenseware.report_components import BaseReportComponent
from typing import List


class ComponentFilterSchema(Schema):
    field_name   = fields.String(required=True)
    filter_type  =  fields.String(required=True)
    filter_value = fields.List(fields.String, required=False)



def create_report_component_resource(component: BaseReportComponent):
    
    class ComponentResource(Resource):
        
        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return component.get_data(request)
        
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return component.get_data(request)
        
        
    return ComponentResource
    


def get_report_components_namespace(ns: Namespace, reports:List[ReportBuilder]):
    
    restx_model = build_restx_model(ns, ComponentFilterSchema)
    
    for report in reports:
        for component in report.components:
            
            RC = create_report_component_resource(component)
            
            @ns.doc(
                id="Get components data with an optional filter payload",
                responses={
                    200 : 'Success',
                    403 : "Missing `Tenantid` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
                body=restx_model
            )
            class TempReportComponentResource(RC): ...
            
            ReportComponentResource = type(
                report.report_id.replace("_", "").capitalize() + 'component',
                (TempReportComponentResource, ),
                {}
            )
            
            ns.add_resource(ReportComponentResource, report.report_path + component.path) 
            
    return ns
        
       
       
       
       