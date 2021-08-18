from flask_restx import Namespace, Resource
from app.licenseware.decorators.auth_decorators import machine_check
from app.licenseware.decorators import failsafe
from app.licenseware.registry_service import register_app
from typing import Type


def get_app_registration_namespace(ns: Namespace, selfapp:Type):
    
    @ns.route(selfapp.register_app_path)
    class AppRegistration(Resource):
        @failsafe(fail_code=500)
        @machine_check
        @ns.doc(
            id="Register app to registry-service",
            responses={
                200 : 'Registration successful',
                403 : "Missing `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        def get(self):
            return register_app(**vars(selfapp)) 
    
    return ns
        
              