from flask import request
from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe


    
def add_uploads_filenames_validation_routes(api: Api, uploaders:list):
    
    for uploader in uploaders:
                
        @api.route("/uploads" + uploader.upload_validation_path)
        class FilenameValidate(Resource): 
            @failsafe(fail_code=500)
            @authorization_check
            @api.doc('Validate file name')
            def post(self):
                return uploader.validate_filenames(request)

    return api
    