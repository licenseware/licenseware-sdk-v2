"""

When this endpoint is called the generated metadata from marshmallow schemas provided in `AppBuilder` at `editable_tables_schemas` parameter will be returned.

See `editable_table` package for more information.

"""

from flask import request
from flask_restx import Api, Resource, fields
from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.utils import tokens






def add_public_token_route(api:Api, appvars:dict):
    
    @api.route(appvars['tokens_path'])
    class PublicToken(Resource):

        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Generate a public token",
            responses={
                200: "Public token",
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            }
        )
        def get(self):
            tenant_id = request.headers.get("TenantId")
            return tokens.get_public_token(tenant_id)
    

        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            description="Delete public token",
            responses={
                200: "Public token deleted",
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            }
        )
        def delete(self):
            tenant_id = request.headers.get("TenantId")
            return tokens.delete_public_token(tenant_id)


    return api


