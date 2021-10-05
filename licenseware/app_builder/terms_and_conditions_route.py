from flask import request
from flask_restx import Api, Resource
from licenseware.decorators import failsafe
from licenseware.utils.logger import log

from licenseware import resources
import importlib.resources as pkg_resources





def add_terms_and_conditions_route(api:Api, appvars:dict):
    
    #TODO template can be updated with custom data using jinja2 (see CLI for more info)
    
    @api.route(appvars['terms_and_conditions_path'])
    class TermsAndConds(Resource): 
        @failsafe(fail_code=500)
        @api.doc(
            description='Return terms and conditions html page', 
            responses={
                200 : 'Terms and Conditions raw html data', 
                500 : 'Something went wrong while handling the request' 
            }
        )
        def get(self):
            
            raw_html = pkg_resources.read_text(resources, "terms_and_conditions.html")
            
            return raw_html
            
    return api


