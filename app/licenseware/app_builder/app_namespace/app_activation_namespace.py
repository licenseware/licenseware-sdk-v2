from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.registry_service import register_app
from app.licenseware.utils.logger import log
from typing import Type



def get_app_activation_namespace(ns: Namespace, selfapp:Type, uploaders:list):
    
    @ns.route(selfapp.app_activation_path)
    class InitializeTenantApp(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @ns.doc(
            id="Initialize app for tenant_id",
            responses={
                200 : 'Quota is within limits',
                400 : "Tenantid not provided",
                402 : 'Quota exceeded',
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        def get(self):
            
            tenant_id = request.headers.get("Tenantid")
            
            if not tenant_id: 
                return {'status': 'fail', 'message': 'Tenantid not provided'}, 403

            for uploader in uploaders:
                log.warning("TODO - Initialize quota for tenant_id")
                # qmsg, _ = uploader.init_tenant_quota(tenant_id)
                
                # if qmsg['status'] != 'success':
                #     return {'status': 'fail', 'message': 'App failed to install'}, 500
            
            dmsg, _ = register_app(**vars(selfapp))
            
            if dmsg['status'] != 'success':
                return {'status': 'fail', 'message': 'App failed to register'}, 500
        
            return {'status': 'success', 'message': 'App installed successfully'}, 200


    return ns
        
              