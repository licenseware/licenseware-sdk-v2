"""

Given a list of filenames return validation analysis response

Notice we are using `build_restx_model` function to generate the swagger body required for the request. 

Notice also the separation of creating the resource and the given namespace. 

"""


from flask import request
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import build_restx_model

from licenseware.uploader_builder import UploaderBuilder
from typing import List



class FilenamesValidationSchema(Schema):
    filenames = fields.List(fields.Str, required=True)
    
    

def create_uploader_resource(uploader:UploaderBuilder):
             
    class FilenameValidate(Resource): 
        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return uploader.validate_filenames(request)
        
    return FilenameValidate



def get_filenames_validation_namespace(ns: Namespace, uploaders:List[UploaderBuilder]):
    
    restx_model = build_restx_model(ns, FilenamesValidationSchema)
    
    for uploader in uploaders:
        
        if uploader.validator_class is None: continue
        
        UR = create_uploader_resource(uploader)
           
        @ns.doc(
            description='Validating the list of filenames provided',
            responses={
                200 : 'Filenames are valid', 
                400 : 'Filenames sent for validation must be in a list of strings format',
                402 : 'Quota exceeded',
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            }
        )
        @ns.expect(restx_model)
        class TempUploaderResource(UR): ...

        
        # Adding extra swagger query parameters if provided
        if uploader.query_params_on_validation:
            
            params_dict = {}
            for param_name, param_description in uploader.query_params_on_validation.items():
                params_dict[param_name] = { 'description': param_description }
            
            TempUploaderResource.__apidoc__.update({'params': params_dict})
        
        
        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + 'filenames',
            (TempUploaderResource, ),
            {}
        )
        
        ns.add_resource(UploaderResource, uploader.upload_validation_path) 
           

    return ns
    





