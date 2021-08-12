from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants import clear_tenant_data 

    
def add_uploads_filestream_validation_routes(api: Api, uploaders:list):
    
    for uploader in uploaders:
            
        @api.route("/uploads" + uploader.upload_path)
        class FileStreamValidate(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @api.doc('Validate file contents')
            @api.doc(params={'clear_data': 'Boolean parameter, warning, will clear existing data'})
            def post(self):
                
                clear_data = request.args.get('clear_data', 'false')
                if 'true' in clear_data.lower():
                    clear_tenant_data(request.headers.get("TenantId"))

                return uploader.upload_files(request)

    return api
