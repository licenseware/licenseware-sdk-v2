import json, os
from flask import request
from flask import send_from_directory
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from marshmallow import Schema, fields
from licenseware.utils.miscellaneous import build_restx_model
from licenseware.utils.logger import log
from licenseware.common.constants import envs

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
            )
            # @ns.expect(restx_model)
            class TempReportComponentResource(RC): ...
            
            ReportComponentResource = type(
                report.report_id.replace("_", "").capitalize() + 'component',
                (TempReportComponentResource, ),
                {}
            )
            
            ns.add_resource(ReportComponentResource, report.report_path + component.path) 
            
    return ns
        
       
       
       
       