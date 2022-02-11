"""

Notice we are using `build_restx_model` function to generate the swagger body required for the request. 
Notice also the separation of creating the resource and the given namespace. 

"""

from typing import List
from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.utils.logger import log

from licenseware.feature_builder import FeatureBuilder



def create_feature_resource(feature:FeatureBuilder):

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




def get_features_namespace(ns: Namespace, features:List[FeatureBuilder]):

    
    for feature in features:
        
        FeatureRes = create_feature_resource(feature)

        update_feature_status_model = ns.model('update_feature_status', dict(
                activated = fields.Boolean(required=True)
            )
        )

        docs = {
            'get': {
                'description': 'Get feature details',
                'responses': { 
                    200: 'Feature details', 
                    403: 'Missing `Tenantid` or `Authorization` information', 
                    500: 'Something went wrong while handling the request'
                }
            },
            'post': {
                'description': 'Set feature status', 
                'validate': True, 
                'expect': [update_feature_status_model], 
                'responses': { 
                    200: 'Success', 
                    403: 'Missing `Tenantid` or `Authorization` information', 
                    500: 'Something went wrong while handling the request'
                }
            }
        }
        
        FeatureRes.__apidoc__ = docs
       

        FeatureResource = type(
            feature.feature_id.replace("_", "").capitalize() + 'Feature',
            (FeatureRes, ),
            {}
        )
        
        ns.add_resource(FeatureResource, feature.feature_path) 

    return ns




    