"""
from licenseware import AppCreator
from ..uploaders import valid_sccm_file



app_id = "mdm-service"


app = dict(
    id=app_id,
    name="Microsoft Deployment Manager service",
    description="This app analyses Microsoft Data from SCCM"
)


uploaders = [
    dict(
    app_id=app_id,
    description="Microsoft Query CSV files",
    upload_name="Microsoft Query CSVs",
    uploader_id="sccm_queries",
    accepted_file_types=".csv",
    validation_function=valid_sccm_file,
    ),
    
]



reports = [
    dict( #same kwargs as in ReportCreator
        app_id=app_id,
        report_id="mdm_history",
        report_name="MDM History Report",
        description="History of MDM actions",
        url='/history_report',
        connected_apps=['mdm-service'],
        # TODO components and filters not created see ReportsCreator
        components=[],#history_components,
        filters=[],#history_filters
    ),

]


MDM = AppCreator(
    app_kwargs=app,
    uploaders_kwargs_list=uploaders,
    reports_kwargs_list=reports,
    editable_tables_schemas_list = []
)


# Then init app in the file where you gather resources 


from flask import Blueprint
from flask_restx import Api

from .main.controller import MDM



blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='mdm-service',
    version='1.0',
    description="Microsoft Data Analysis App"
)


api = MDM.init_app(api)


api.add_namespace(etc)


"""

from typing import List
from flask import request
from flask_restx import Namespace, Resource
from licenseware.namespace_generator.schema_namespace import auth_header_doc
from licenseware.editable_table import editable_tables_from_schemas
from licenseware.report_creator import ReportCreator
from licenseware.registry import (
    AppDefinition, 
    Uploader
)


from licenseware.decorators.failsafe_decorator import failsafe
from licenseware.decorators.auth_decorators import authorization_check, machine_check

from .tenant_utils import TenantUtils
from licenseware.utils.urls import URL_PREFIX
from licenseware.auth import Authenticator




class AppCreator:
    def __init__(
        self, 
        app_kwargs: dict,
        uploaders_kwargs_list: List[dict],
        reports_kwargs_list: List[dict],
        **kwargs
    ):
        self.app_kwargs = app_kwargs
        self.uploaders_kwargs_list = uploaders_kwargs_list
        self.reports_kwargs_list = reports_kwargs_list
        self.kwargs = kwargs
        
        self.ns = None
        
        self.tenant_utils = None 
        self.app_definition = None
        
        self.uploaders = None
        self.reports = None
        self.reports_api = None
        
        
    def init_app(self, api):
        
        Authenticator.connect()
        
        api.add_namespace( self.api, path=URL_PREFIX )

        for report in self.reports_api:
            api.add_namespace( report, path=URL_PREFIX + "/reports" )
            
        return api


        
    @property
    def api(self):
        return self.initialize()
        
        
    def initialize(self):
        # Entrypoint
        
        self.init_tenant_utils()
        self.init_app_definition()
        self.init_uploaders()
        self.init_reports()
        
        self.create_namespace()
        
        self.add_app_route()
        self.add_app_activation_route()
        self.add_register_all_route()
        self.add_editable_tables_route()
        
        self.add_uploads_filenames_validation_routes()
        self.add_uploads_filestream_validation_routes()
        self.add_uploads_status_routes()
        self.add_uploads_quota_routes()
        self.add_tenant_registration_url()

        if not self.kwargs.get('disable_registration', False):
        
            self.app_definition.register_all(
                uploaders = self.uploaders if self.uploaders is not None else [],
                reports   = self.reports if self.reports is not None else [],
            )
        
        return self.ns
        
        
    def init_reports(self):
        
        self.reports = []
        self.reports_api = []
        for kwargs in self.reports_kwargs_list:
            r = ReportCreator(**kwargs)
            self.reports.append(r.report)
            self.reports_api.append(r.api)
            setattr(AppCreator, r.report_id + '_report', r.report)
            setattr(AppCreator, r.report_id + '_api', r.api)
            
    
    def init_uploaders(self):
        
        self.uploaders = []
        for kwargs in self.uploaders_kwargs_list:
            u = Uploader(**kwargs)
            self.uploaders.append(u)
            setattr(AppCreator, u.uploader_id + '_uploader', u) 
        
        
                
    def init_tenant_utils(self):
        
        self.tenant_utils = TenantUtils(
            data_collection_name = self.kwargs.get('data_collection_name'),
            utilization_collection_name = self.kwargs.get('utilization_collection_name'),
            analysis_collection_name = self.kwargs.get('analysis_collection_name')
        )
        
        if not self.kwargs.get('processing_status_func'):
            self.kwargs['processing_status_func'] = self.tenant_utils.get_processing_status
        
        if not self.kwargs.get('clear_tenant_data_func'):
            self.kwargs['clear_tenant_data_func'] = self.tenant_utils.clear_tenant_data
        
        
    def init_app_definition(self):
        
        if not self.app_kwargs.get('activated_tenants_func'):
            self.app_kwargs['activated_tenants_func'] = self.tenant_utils.get_activated_tenants
            
        if not self.app_kwargs.get('tenants_with_data_func'):
            self.app_kwargs['tenants_with_data_func'] = self.tenant_utils.get_tenants_with_data
    
        self.app_definition = AppDefinition(**self.app_kwargs)
        
        
        
    def create_namespace(self):
        
        self.ns = Namespace(
            name = self.app_kwargs['name'], 
            description = self.app_kwargs['description'],
            authorizations = auth_header_doc,
            security = list(auth_header_doc.keys())
        )
                
                
    def add_register_all_route(self):
        
        app_definition, reports, uploaders = self.app_definition, self.reports, self.uploaders
        
        class RegisterAll(Resource):
            @machine_check
            @self.ns.doc("Register all reports and uploaders")
            def get(self):
                
                response_ok = app_definition.register_all(
                    reports = reports, 
                    uploaders = uploaders
                )
                
                if response_ok:
                    return {
                            "status": "success",
                            "message": "Reports and uploaders registered successfully"
                        }, 200
                else:
                    return {
                            "status": "fail",
                            "message": "Reports and uploaders registering failed"
                        }, 500
                    
        
        self.ns.add_resource(RegisterAll, '/register_all')
        
                    
    def add_editable_tables_route(self):
        
        kwargs = self.kwargs
        
        class EditableTables(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            @self.ns.doc("Get Editable tables shape")
            def get(self):
                    return editable_tables_from_schemas(
                        kwargs['editable_tables_schemas_list']
                    )
        
        self.ns.add_resource(EditableTables, '/editable_tables')
                    
                         
    def add_app_route(self):
        
        app_definition = self.app_definition
        
        class AppRegistration(Resource):
            @failsafe(fail_code=500)
            @machine_check
            @self.ns.doc("Send post with app information to /apps")
            def get(self):
                return app_definition.register_app() 
            
        self.ns.add_resource(AppRegistration, '/app')
                  
                  
    def add_app_activation_route(self):
        
        app_definition, uploaders = self.app_definition, self.uploaders
        
        
        class InitializeTenantApp(Resource):
            @failsafe(fail_code=500)
            @authorization_check
            @self.ns.doc("Initialize app for tenant_id")
            def get(self):
                
                tenant_id = request.headers.get("TenantId")

                for uploader in uploaders:
                    qmsg, _ = uploader.init_quota(tenant_id)
                    if qmsg['status'] != 'success':
                        return {'status': 'fail', 'message': 'App failed to install'}, 500
                
                dmsg, _ = app_definition.register_app()
                
                if dmsg['status'] != 'success':
                    return {'status': 'fail', 'message': 'App failed to register'}, 500
            
                return {'status': 'success', 'message': 'App installed successfully'}, 200

                    
        self.ns.add_resource(InitializeTenantApp, '/app/init')


    def add_uploads_filenames_validation_routes(self):
                    
        for uploader in self.uploaders:
                
            class FilenameValidate(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Validate file name')
                def post(self):
                    return uploader.validate_filenames(request)

            self.ns.add_resource(FilenameValidate, "/uploads" + uploader.upload_validation_url)

    
    def add_uploads_filestream_validation_routes(self):
                    
        for uploader in self.uploaders:
            
            class FileStreamValidate(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Validate file contents')
                @self.ns.doc(params={'clear_data': 'Boolean parameter, warning, will clear existing data'})
                def post(self):
                    
                    clear_data = request.args.get('clear_data', 'false')
                    if 'true' in clear_data.lower():
                        self.kwargs['clear_tenant_data_func'](request.headers.get("TenantId"))

                    return uploader.upload_files(request)

            self.ns.add_resource(FileStreamValidate, "/uploads" + uploader.upload_url)

        
    def add_uploads_quota_routes(self):
                    
        for uploader in self.uploaders:
                                
            class UploaderQuota(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Check if tenant has quota within limits') 
                def get(self):
                    return uploader.check_quota(request.headers.get("TenantId"))
                
            self.ns.add_resource(UploaderQuota, "/uploads" + uploader.quota_validation_url)
            

    def add_uploads_status_routes(self):
          
        for uploader in self.uploaders:
                  
            class UploaderStatus(Resource): 
                @failsafe(fail_code=500)
                @authorization_check
                @self.ns.doc('Get processing status of files uploaded') 
                def get(self):
                    return self.kwargs['processing_status_func'](request.headers.get("TenantId")) 
                
            self.ns.add_resource(UploaderStatus, "/uploads" + uploader.status_check_url)
            
            
    def add_tenant_registration_url(self):
        
        tenant_utils = self.tenant_utils
        
        class TenantRegistration(Resource): 
            @failsafe(fail_code=500)
            @machine_check
            @self.ns.doc('Get `app_activated` and `data_available` boleans for tenant_id')
            @self.ns.doc(params={'tenant_id': 'Tenant ID for which the info is requested'})
            def get(self):
                
                tenant_id = request.args.get('tenant_id')
                
                if tenant_id:
                    
                    return {
                        "app_activated": bool(tenant_utils.get_tenants_with_data(tenant_id)),
                        "data_available": bool(tenant_utils.get_activated_tenants(tenant_id))
                    }
    
                return {'status': 'fail', 'message': 'Query parameter `tenant_id` not provided'}
        
        self.ns.add_resource(TenantRegistration, self.app_definition.tenant_registration_url)
