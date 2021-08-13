from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.decorators import failsafe
from app.licenseware.registry_service import register_app



def add_app_route(api: Api, app_vars:dict):
    @api.route('/app')
    class AppRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc("Send post with app information to /apps")
        def get(self):
            return register_app(**app_vars) 
    
    return api
        
              