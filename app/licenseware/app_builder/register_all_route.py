from flask_restx import Api, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.registry_service import register_all
from app.licenseware.decorators import failsafe




def add_register_all_route(api, reports, uploaders):
    
    @api.route('/register_all')
    class RegisterAll(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc("Register all reports and uploaders")
        def get(self):
            
            response_ok = register_all(
                reports = reports, 
                uploaders = uploaders
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
                
