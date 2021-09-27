from flask import request
from marshmallow import Schema, fields

from flask_restx import Namespace, Resource

from licenseware.utils.logger import log
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.report_components.base_report_component import BaseReportComponent
from licenseware.utils.miscellaneous import build_restx_model
from licenseware.decorators import failsafe

from licenseware.download import download_as




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
            
            file_type = request.args.get('download_as')
            tenant_id = request.headers.get('Tenantid')
            data = component.get_data(request)
                
            if file_type is None: 
                return data
            
            return download_as(
                file_type, 
                data, 
                tenant_id, 
                filename=component.component_id
            )
            
                
    return ReportComponent
    
    
    

def get_report_individual_components_namespace(ns: Namespace, report_components:list):
    
    restx_model = build_restx_model(ns, ComponentFilterSchema)

    for comp in report_components:
        
        IRC = create_individual_report_component_resource(comp)
            
        @ns.doc(
            id="Get component data with an optional filter payload",
            params={'download_as': 'Download table component as file type: csv, xlsx, json'},
            responses={
                200 : 'Success',
                403 : "Missing `Tenantid` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            }
        )
        # @ns.expect(restx_model)
        class TempIndvReportComponentResource(IRC): ...
            
        IndvReportComponentResource = type(
            comp.component_id.replace("_", "").capitalize() + 'individual_component',
            (TempIndvReportComponentResource, ),
            {}
        )
        
        ns.add_resource(IndvReportComponentResource, comp.component_path) 
    
    return ns
        
       
       
       