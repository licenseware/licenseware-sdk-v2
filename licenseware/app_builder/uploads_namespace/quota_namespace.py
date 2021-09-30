from flask import request
from flask_restx import Namespace, Resource
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.decorators import failsafe


from licenseware.uploader_builder import UploaderBuilder
from typing import List



def create_uploader_resource(uploader: UploaderBuilder):
    
    class UploaderQuota(Resource): 
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return uploader.check_tenant_quota(
                request.headers.get("Tenantid")
            )
            
    return UploaderQuota

    

def get_quota_namespace(ns: Namespace, uploaders:List[UploaderBuilder]):
                
    for uploader in uploaders:
        
        if uploader.quota_units is None: continue
    
        UR = create_uploader_resource(uploader)
                     
        @ns.doc(
            id='Check if tenant has quota within limits',
            responses={
                200 : 'Quota is within limits',
                400 : "Tenantid not provided",
                402 : 'Quota exceeded',
                403 : "Missing `Tenant` or `Authorization` information",
                500 : 'Something went wrong while handling the request' 
            },
        )
        class TempUploaderResource(UR): ...
        
        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + 'quota',
            (TempUploaderResource, ),
            {}
        )
        
        ns.add_resource(UploaderResource, uploader.quota_validation_path) 
                
    return ns


