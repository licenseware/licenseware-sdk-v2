from flask import request
from flask_restx import Namespace, Resource

from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.utils.logger import log


def get_filenames_validation_namespace(ns: Namespace, uploaders:list):
    
    for uploader in uploaders:
                
        @ns.route(uploader.upload_validation_path)
        class FilenameValidate(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @ns.doc(
                id='Validate file name list',
                responses={
                    200 : 'Filenames are valid', 
                    400 : 'Filenames sent for validation must be in a list of strings format',
                    402 : 'Quota exceeded',
                    403 : "Missing `Tenant` or `Authorization` information",
                    500 : 'Something went wrong while handling the request' 
                }
            )
            def post(self):
                return uploader.validate_filenames(request)

    return ns
    
