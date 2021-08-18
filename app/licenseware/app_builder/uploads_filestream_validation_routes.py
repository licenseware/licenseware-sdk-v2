from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.tenants import clear_tenant_data 
from werkzeug.datastructures import FileStorage


    
def add_uploads_filestream_validation_routes(api: Api, uploaders:list):
    
    
    file_upload_parser = api.parser()
    file_upload_parser.add_argument(
        'files[]', 
        location='files', 
        type=FileStorage, 
        required=True, 
        help="Upload files for processing"
    )

    
    for uploader in uploaders:
            
        @api.route("/uploads" + uploader.upload_path)
        class FileStreamValidate(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @api.doc('Validate file contents')
            @api.doc(
                params={'clear_data': 'Boolean parameter, warning, will clear existing data'},
                responses={
                    200 : 'Files are valid',
                    400 : "File list is empty or files are not on 'files[]' key",
                    402 : 'Quota exceeded',
                    403 : "Missing `Tenant` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            @api.expect(file_upload_parser)
            def post(self):
                
                clear_data = request.args.get('clear_data', 'false')
                if 'true' in clear_data.lower():
                    clear_tenant_data(request.headers.get("TenantId"))

                return uploader.upload_files(request)

    return api
