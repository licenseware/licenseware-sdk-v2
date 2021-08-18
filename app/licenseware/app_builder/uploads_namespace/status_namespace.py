from flask import request
from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants.processing_status import get_processing_status



def get_status_namespace(ns: Namespace, uploaders:list):
        
    for uploader in uploaders:
                
        @ns.route(uploader.status_check_path)
        class UploaderStatus(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id='Get processing status of files uploaded',
                responses={
                    # 200 : '',
                    400 : "Tenantid not provided",
                    403 : "Missing `Tenant` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            ) 
            def get(self):
                return get_processing_status(request.headers.get("TenantId")) 
            
    return ns
