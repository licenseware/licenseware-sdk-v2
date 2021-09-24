import json, os
from flask import request
from flask import send_from_directory
from marshmallow import Schema, fields

from flask_restx import Namespace, Resource

from licenseware.utils.logger import log
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.report_components.base_report_component import BaseReportComponent
from licenseware.utils.miscellaneous import build_restx_model
from licenseware.decorators import failsafe
from licenseware.common.constants import envs





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
    
            if file_type:
                
                data = component.get_data(request)
            
                filename = f'{component.component_id}.json'
                dirpath = envs.get_tenant_upload_path(tenant_id)
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'w') as outfile: json.dump(data, outfile)
                
                return send_from_directory(
                    directory=dirpath, 
                    filename=filename, 
                    as_attachment=True
                )
                
            return component.get_data(request)
        
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
        
       
       
       