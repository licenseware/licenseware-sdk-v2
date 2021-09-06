from flask import request
from flask_restx import Namespace, Resource 

from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from licenseware.tenants import clear_tenant_data 
from werkzeug.datastructures import FileStorage


    
def get_filestream_validation_namespace(ns: Namespace, uploaders:list):
    
    
    file_upload_parser = ns.parser()
    file_upload_parser.add_argument(
        'files[]', 
        location='files', 
        type=FileStorage, 
        required=True, 
        help="Upload files for processing"
    )

    
    for uploader in uploaders:
            
        @ns.route(uploader.upload_path)
        class FileStreamValidate(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id='Validate file contents',
                params={'clear_data': 'Boolean parameter, warning, will clear existing data'},
                responses={
                    200 : 'Files are valid',
                    400 : "File list is empty or files are not on 'files[]' key",
                    402 : 'Quota exceeded',
                    403 : "Missing `Tenant` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                },
            )
            @ns.expect(file_upload_parser)
            def post(self):
                
                clear_data = request.args.get('clear_data', 'false')
                if 'true' in clear_data.lower():
                    clear_tenant_data(request.headers.get("TenantId"))

                return uploader.upload_files(request)

    return ns
