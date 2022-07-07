from typing import List
from flask import request
from flask_restx import Namespace, Resource, fields
from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.report_builder import ReportBuilder


def create_report_snapshot_resource(report: ReportBuilder):

    class ReportController(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            
            version = request.args.get('version')
            component_id = request.args.get('component_id')
            
            if version is None:
                return report.get_available_versions(request)
        
            if component_id is None:
                return report.get_snapshot_metadata(request)

            return report.get_snapshot_component(request)


        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            
            version = request.args.get('version')
            component_id = request.args.get('component_id')
            
            if version is None and component_id is None:
                return "Parameter `version` and `component_id` must be specified", 400

            return report.get_snapshot_component(request)



        @failsafe(fail_code=500)
        @authorization_check
        def put(self):
            
            version = request.args.get('version')
            component_id = request.args.get('component_id')
            
            if version is None:
                return "Parameter `version` must be specified", 400

        
        @failsafe(fail_code=500)
        @authorization_check
        def delete(self):
            
            version = request.args.get('version')
            component_id = request.args.get('component_id')
            
            if version is None:
                return "Parameter `version` must be specified", 400
        
        
    return ReportController


def get_report_snapshot_namespace(ns: Namespace, reports: List[ReportBuilder]):

    restx_model = ns.model('ComponentFilter', dict(
        column=fields.String,
        filter_type=fields.String,
        filter_value=fields.List(fields.String)
    ))

    for report in reports:

        RR = create_report_snapshot_resource(report)
        
        docs = {
            'post': {
                'description': "Get component data with an optional filter payload",
                'validate': None,
                'expect': [restx_model],
                'params': {
                    'version': {'description': 'Snapshot version'},
                    'component_id': {'description': "Get data for this component. Make sure to fill the version."},
                    'limit': {'description': "Limit number of results for this component_id."},
                    'skip': {'description': "Skip/Offset number of results for this component_id."},
                },
            },
            'get': {
                'description': "Get static report version of this report",
                'params': {
                    'version': {
                        'description': """
If empty will return available versions: 
```
{
    "versions": ["XFHDFD", etc]
}
```
If filled will the return snapshot metadata for this version.
""",
},
                'component_id': {'description': "Get data for this component. Make sure to fill the version."},
                'limit': {'description': "Limit number of results for this component_id."},
                'skip': {'description': "Skip/Offset number of results for this component_id."},
                },
                'responses': {
                    200: 'Success',
                    403: 'Missing `Tenantid` or `Authorization` information',
                    500: 'Something went wrong while handling the request'
                }
            }
        }

        RR.__apidoc__ = docs

        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + 'snapshot',
            (RR,),
            {}
        )

        ns.add_resource(ReportResource, report.report_path + "/snapshot")

    return ns
