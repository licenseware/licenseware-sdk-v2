from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import authorization_check
from app.licenseware.decorators import failsafe
from app.licenseware.editable_tables import editable_tables_from_schemas


def add_editable_tables_route(api, editable_tables_schemas:list):
    
    @api.route('/editable_tables')
    class EditableTables(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        @api.doc("Get editable tables metadata")
        def get(self):
            return editable_tables_from_schemas(
                editable_tables_schemas
            )
    
    return api


