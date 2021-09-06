from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe



def get_quota_namespace(ns: Namespace, uploaders:list):
                
    for uploader in uploaders:
               
        @ns.route(uploader.quota_validation_path)             
        class UploaderQuota(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id='Check if tenant has quota within limits',
                responses={
                    200 : 'Quota is within limits',
                    400 : "Tenantid not provided",
                    402 : 'Quota exceeded',
                    403 : "Missing `Tenant` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            ) 
            def get(self):
                return uploader.check_tenant_quota(
                    request.headers.get("Tenantid")
                )
                
    return ns

