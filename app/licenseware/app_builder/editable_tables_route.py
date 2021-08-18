from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.editable_tables import editable_tables_from_schemas



def add_editable_tables_route(api:Api, appvars:dict):
    
    @api.route(appvars['editable_tables_path'])
    class EditableTables(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc(
            id="Get editable tables metadata",
            responses={
                200 : 'TODO - add doc',
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        def get(self):
            return editable_tables_from_schemas(
                appvars['editable_tables_schemas']
            )
    
    return api


