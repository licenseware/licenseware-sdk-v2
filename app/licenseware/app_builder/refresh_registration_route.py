from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.registry_service import register_all
from app.licenseware.decorators import failsafe
from app.licenseware.utils.logger import log


def add_refresh_registration_route(api:Api, appvars:dict):
    
    @api.route(appvars['refresh_registration_path'])
    class RefreshRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            id="Register all reports and uploaders",
            responses={
                200 : 'Registering process was successful',
                403 : "Missing `Authorization` information",
                500 : 'Registering process was unsuccessful' 
            },
        )
        def get(self):
            
            # Converting from objects to dictionaries
            reports   = [vars(r) for r in appvars['reports']]
            uploaders = [vars(u) for u in appvars['uploaders']]
            
            response, status_code = register_all(
                app = appvars,
                reports = reports, 
                uploaders = uploaders
            )
            
            log.debug(response)
            
            return response, status_code
            
            
    return api
                
