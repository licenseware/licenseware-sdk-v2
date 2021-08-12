from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants.processing_status import get_processing_status



def add_uploads_quota_routes(api: Api, uploaders:list):
                
    for uploader in uploaders:
               
        @api.route("/uploads" + uploader.quota_validation_path)             
        class UploaderQuota(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @api.doc('Check if tenant has quota within limits') 
            def get(self):
                return uploader.check_tenant_quota(request.headers.get("TenantId")) 
            #TODO separate check_tenant_quota func from uploader
            
    return api

