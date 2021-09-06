"""

When this endpoint is called info about Tenant `App` activation and utilization will be returned.

"""


from flask import request
from flask_restx import Api, Resource
from licenseware.decorators.auth_decorators import machine_check
from licenseware.decorators import failsafe
from licenseware.tenants import  get_activated_tenants, get_tenants_with_data



def add_tenant_registration_route(api:Api, appvars:dict):
    
    @api.route(appvars['tenant_registration_path'])
    class TenantRegistration(Resource): 
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            id='Get `app_activated` and `data_available` boleans for tenant_id', 
            params={'tenant_id': 'Tenant ID for which the info is requested'},
            responses={
                200 : 'Json with `app_activated`, `data_available` for `tenant_id`', 
                400 : 'Query parameter `tenant_id` not provided',
                403 : "Missing `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            }
        )
        def get(self):
            
            tenant_id = request.args.get('tenant_id')
            
            if tenant_id:
                
                return {
                    "app_activated": bool(get_tenants_with_data(tenant_id)),
                    "data_available": bool(get_activated_tenants(tenant_id))
                }, 200

            return {
                'status': 'fail', 
                'message': 'Query parameter `tenant_id` not provided'
            }, 400
    
    
    return api

