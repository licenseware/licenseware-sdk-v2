from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.registry_service import register_all
from app.licenseware.decorators import failsafe



def add_refresh_registration_route(api:Api, appvars:dict):
    
    @api.route(appvars['refresh_registration_path'])
    class RefreshRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            id="Register all reports and uploaders",
            responses={
                200 : 'TODO - add doc',
                403 : "Missing `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        def get(self):
            
            response_ok = register_all(
                app = appvars,
                reports = appvars['reports'], 
                uploaders = appvars['uploaders']
            )
            
            if response_ok:
                return {
                        "status": "success",
                        "message": "Reports and uploaders registered successfully"
                    }, 200
            else:
                return {
                        "status": "fail",
                        "message": "Reports and uploaders registering failed"
                    }, 500
                
    return api
                
