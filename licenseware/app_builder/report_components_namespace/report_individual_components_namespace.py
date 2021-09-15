from licenseware.report_components.base_report_component import BaseReportComponent
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



def create_individual_report_component_resource(component: BaseReportComponent):
    
    class ReportComponent(Resource):
        
        @failsafe(fail_code=500)
        @authorization_check        
        def post(self):
            return component.get_data(request)
    
        @failsafe(fail_code=500)
        @authorization_check        
        def get(self):
            return component.get_data(request)
        
    return ReportComponent
    
    
    

def get_report_individual_components_namespace(ns: Namespace, report_components:list):
    
    restx_model = build_restx_model(ns, ComponentFilterSchema)

    for comp in report_components:
        
        IRC = create_individual_report_component_resource(comp)
            
        @ns.doc(
            id="Get component data with an optional filter payload",
            responses={
                200 : 'Success',
                403 : "Missing `Tenantid` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
            body=restx_model
        )
        class TempIndvReportComponentResource(IRC): ...
            
        IndvReportComponentResource = type(
            comp.component_id.replace("_", "").capitalize() + 'individual_component',
            (TempIndvReportComponentResource, ),
            {}
        )
        
        ns.add_resource(IndvReportComponentResource, comp.component_path) 
    
    return ns
        
       
       
       