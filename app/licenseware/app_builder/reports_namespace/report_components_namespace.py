from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe



def get_report_components_namespace(ns: Namespace, reports:list):
    
    for report in reports:
        
        @ns.route(report.report_path)
        class ReportController(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id="Get components metadata",
                responses={
                    200 : 'Success',
                    403 : "Missing `Tenantid` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            def get(self):
                return report.return_json_payload()
            
            
            
    return ns
        
       


def create_component_resource(self, Report, data):
    
    class Data:
            component_id = data['component_id']
            
    class BaseResource(Resource):
        
        @failsafe(fail_code=500)
        @self.ns.doc(f"Get data for {Data.component_id}")
        def get(self):
            
            return Report.components[Data.component_id].return_component_data(_request=request)
        
        @failsafe(fail_code=500)
        @self.ns.doc(f"Filter data for {Data.component_id}")
        @self.ns.marshal_list_with(self.filter_model)
        def post(self):
            filter_payload = request.json
            parsed_filters = Report._filter.build_match_expression(filter_payload)
            return Report.components[Data.component_id].return_component_data(_request=request, _filter=parsed_filters)
    
    
    ComponentResource = type(
        "Report_" + Data.component_id, 
        (BaseResource, Data), 
        {}
    )
    
    
    return ComponentResource, Report.return_component_url(Data.component_id)
    
    
def add_components_routes(self):
    
    Report = self.standard_report
    
    for data, _ in self.components:
        
        ComponentResource, url = self.create_component_resource(Report, data)
        
        self.ns.add_resource( ComponentResource, url ) 
        
        
        
