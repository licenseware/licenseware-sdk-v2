"""
Here we have the uploader route builder section.
Each time we have a list of entities we need to create a new route or a similar route, like we have below.
We need to separate the resource from the restx namespace, otherwise the resource will be overwrited.

"""


from flask import request
from flask_restx import Namespace, Resource 

from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from licenseware.tenants import clear_tenant_data 
from werkzeug.datastructures import FileStorage



    
def create_uploader_resource(uploader):
    
    class FileStreamValidate(Resource): 
        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            
            clear_data = request.args.get('clear_data', 'false')
            if 'true' in clear_data.lower():
                clear_tenant_data(request.headers.get("Tenantid"))

            return uploader.upload_files(request)
        
    return FileStreamValidate


    
    
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
        
        UR = create_uploader_resource(uploader)
        
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
        class TempUploaderResource(UR): ...
        
        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize(),
            (TempUploaderResource, ),
            {}
        )
        
        ns.add_resource(UploaderResource, uploader.upload_path) 
        
    return ns



