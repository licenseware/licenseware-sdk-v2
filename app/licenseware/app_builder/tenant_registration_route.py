from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants import  get_activated_tenants, get_tenants_with_data



def add_tenant_registration_route(api: Api):


    class TenantRegistration(Resource): 
        @failsafe(fail_code=500)
        @machine_check
        @api.doc('Get `app_activated` and `data_available` boleans for tenant_id')
        @api.doc(params={'tenant_id': 'Tenant ID for which the info is requested'})
        def get(self):
            
            tenant_id = request.args.get('tenant_id')
            
            if tenant_id:
                
                return {
                    "app_activated": bool(tenant_utils.get_tenants_with_data(tenant_id)),
                    "data_available": bool(tenant_utils.get_activated_tenants(tenant_id))
                }

            return {'status': 'fail', 'message': 'Query parameter `tenant_id` not provided'}
    
    self.ns.add_resource(TenantRegistration, self.app_definition.tenant_registration_url)




def add_uploads_status_routes(api: Api, uploaders:list):
        
    for uploader in uploaders:
                
        @api.route("/uploads" + uploader.status_check_path)
        class UploaderStatus(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @api.doc('Get processing status of files uploaded') 
            def get(self):
                return get_processing_status(request.headers.get("TenantId")) 
            
    return api
