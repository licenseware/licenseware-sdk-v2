"""

When this endpoint is called the registration information from all `App` entities (uploaders, reports etc) are sent to registry service.

"""


from flask_restx import Api, Resource
from licenseware.decorators.auth_decorators import machine_check
from licenseware.registry_service import register_all
from licenseware.decorators import failsafe
from licenseware.utils.logger import log


def add_refresh_registration_route(api:Api, appvars:dict):
    
    @api.route(appvars['refresh_registration_path'])
    class RefreshRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @api.doc(
            description="Register all reports and uploaders",
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
            report_components = [vars(rv) for rv in appvars['report_components']]
            
            response, status_code = register_all(
                app = appvars,
                reports = reports, 
                report_components = report_components, 
                uploaders = uploaders
            )
            
            return response, status_code
            
            
    return api
                
