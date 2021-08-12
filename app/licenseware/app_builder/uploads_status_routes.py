from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants.processing_status import get_processing_status



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
