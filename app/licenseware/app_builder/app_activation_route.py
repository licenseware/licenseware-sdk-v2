from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.registry_service import register_app
from app.licenseware.utils.logger import log




def add_app_activation_route(api: Api, app_vars:dict, uploaders:list):
    
    @api.route('/app/init')
    class InitializeTenantApp(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc("Initialize app for tenant_id")
        def get(self):
            
            tenant_id = request.headers.get("Tenantid")
            
            if not tenant_id: 
                return {'status': 'fail', 'message': 'Tenantid not provided'}, 403

            for uploader in uploaders:
                log.warning("TODO - Initialize quota for tenant_id")
                # qmsg, _ = uploader.init_tenant_quota(tenant_id)
                
                # if qmsg['status'] != 'success':
                #     return {'status': 'fail', 'message': 'App failed to install'}, 500
            
            dmsg, _ = register_app(**app_vars)
            
            if dmsg['status'] != 'success':
                return {'status': 'fail', 'message': 'App failed to register'}, 500
        
            return {'status': 'success', 'message': 'App installed successfully'}, 200


    return api
        
              