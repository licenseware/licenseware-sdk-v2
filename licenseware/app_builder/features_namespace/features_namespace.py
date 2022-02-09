"""

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

from typing import List

from licenseware.feature_builder import FeatureBuiler



# class FilenamesValidationSchema(Schema):
#     filenames = fields.List(fields.Str, required=True)
    
    

# def create_uploader_resource(uploader:UploaderBuilder):
             
#     class FilenameValidate(Resource): 
#         @failsafe(fail_code=500)
#         @authorization_check
#         def post(self):
#             return uploader.validate_filenames(request)
        
#     return FilenameValidate


class FeaturesSchema(Schema):
    name = fields.String(required=True)
    activated = fields.Boolean(required=True)



def create_feature_resource(feature:FeatureBuiler):

    class Feature(Resource): 

        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return feature.get_status(request)

        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return feature.update_status(request)
    
    return Feature




def get_features_namespace(ns: Namespace, features:List[FeatureBuiler]):

    
    for feature in features:
        pass


    return ns


    

    # restx_model = build_restx_model(ns, FilenamesValidationSchema)
    
    # for uploader in uploaders:
        
    #     if uploader.validator_class is None: continue
        
    #     UR = create_uploader_resource(uploader)
           
    #     @ns.doc(
    #         description='Validating the list of filenames provided',
    #         responses={
    #             200 : 'Filenames are valid', 
    #             400 : 'Filenames sent for validation must be in a list of strings format',
    #             402 : 'Quota exceeded',
    #             403 : "Missing `Tenant` or `Authorization` information",
    #             500 : 'Something went wrong while handling the request' 
    #         }
    #     )
    #     @ns.expect(restx_model)
    #     class TempUploaderResource(UR): ...

        
    #     # Adding extra swagger query parameters if provided
    #     if uploader.query_params_on_validation:
            
    #         params_dict = {}
    #         for param_name, param_description in uploader.query_params_on_validation.items():
    #             params_dict[param_name] = { 'description': param_description }
            
    #         TempUploaderResource.__apidoc__.update({'params': params_dict})
        
        
    #     UploaderResource = type(
    #         uploader.uploader_id.replace("_", "").capitalize() + 'filenames',
    #         (TempUploaderResource, ),
    #         {}
    #     )
        
    #     ns.add_resource(UploaderResource, uploader.upload_validation_path) 
           

    # return ns
    






# @ns.route('/admin/activate-deactivate-product-requests-plugin')
# class ActivateDeactivateProductRequestsPluginAdmin(Resource):

#     @failsafe(fail_code=500)
#     @access_level(rights.CAN_UPDATE_CATALOG)
#     @ns.expect(prm_global_enable_disable_products, validate=True)
#     @ns.doc(description="Activate/Deactivate product requests on all catalogs and products")
#     @ns.response(200, description="Requests updated", model=None) 
#     def post(self):
#         return on_off_product_requests_plugin(request)


# from flask import Request
# from licenseware import mongodata
# from app.common.constants import collections
# from app.serializers.app_settings_schema import AppSettingsSchema as schema



# def on_off_product_requests_plugin(flask_request: Request):
    
#     tenant_id = flask_request.headers.get("TenantId")
#     product_requests_allowed = flask_request.json["product_requests_allowed"]
    
#     updated_nr = mongodata.update(
#         schema=schema,
#         match={'tenant_id': tenant_id},
#         new_data={
#             'tenant_id': tenant_id,
#             'product_requests_allowed': product_requests_allowed
#         },
#         collection=collections.SETTINGS
#     )
    
#     return "Requests updated", 200
    
    
    
    
    
    


# @ns.route('/state-of-product-requests-plugin')
# class CurrentStateOfProductRequestPlugin(Resource):

#     @failsafe(fail_code=500)
#     @ns.doc(description="Returns the current state of the 'Product Request' plugin/feature")
#     @ns.response(200, description="Returns True/False which is means activated/deactivated", model=fields.Boolean) 
#     def get(self):
#         return current_state_of_product_requests_plugin(request)


# from flask import Request
# from licenseware import mongodata
# from app.common.constants import collections



# def current_state_of_product_requests_plugin(flask_request: Request):
    
#     tenant_id = flask_request.headers.get("TenantId")
    
#     results = mongodata.fetch(
#         match={'tenant_id': tenant_id},
#         collection=collections.SETTINGS
#     )
    
#     if not results: return False, 200
    
#     return results[0]['product_requests_allowed'], 200
    
    
    
    
    
    