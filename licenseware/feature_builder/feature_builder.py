import requests
from typing import List
from flask import Request
from licenseware.quota import Quota
from licenseware import mongodata
from licenseware.common.constants import envs
# from licenseware.common.serializers import WildSchema
from licenseware.tenants.user_utils import get_user_tables



class FeatureBuiler:

    def __init__(self,
        name:str,
        description:str = None, 
        access_levels: List[str] = None,
        free_quota:int = 1, 
        activated:bool = False,
        feature_id:str = None,
        feature_path:str = None
    ):
        self.name = name
        self.description = description
        self.access_levels = access_levels
        self.free_quota = free_quota
        self.activated = activated
        self.feature_id = feature_id
        self.feature_path = feature_path
       

    def get_details(self):
        
        #! There can't be 2 features with the same `name`
        # `decorators` will be applied on the route created
        # `access_levels` will be verified with auth 
        #  Ex: 
        #  access_levels = ['admin'] will check 
        #  `shared_tenant` table `access_level` column for `admin` value
        #  or if user is the tenant owner

        if self.feature_id is None:
            self.feature_id = self.name.lower().replace(" ", "_")

        if self.feature_path is None:
            self.feature_path = '/' + self.feature_id.replace("_", "-")

        return {
            'name':self.name,
            'description':self.description,
            'access_levels': self.access_levels,
            'free_quota':self.free_quota,
            'activated':self.activated,
            'feature_id':self.feature_id,
            'feature_path':self.feature_path
        }


    def update_quota(self, flask_request: Request, units:int = 1):
        
        q = Quota(
            tenant_id=flask_request.headers.get("TenantId"),
            auth_token=flask_request.headers.get("Authorization"),
            units=self.free_quota,
            uploader_id=self.feature_id
        )
        
        res, status_code = q.check_quota(units)
        if status_code == 200:
            return q.update_quota(units)
        
        return res, status_code


    def get_status(self, flask_request: Request):

        tenant_id = flask_request.headers.get("TenantId")
    
        results = mongodata.fetch(
            match={'tenant_id': tenant_id},
            collection=envs.MONGO_COLLECTION_FEATURES_NAME
        )
        
        if not results: return False, 200

        return results, 200



    def update_status(self, flask_request: Request):

        data = flask_request.json
        tenant_id = flask_request.headers.get("TenantId")
        auth_token = flask_request.headers.get("Authorization")

        user_tables = get_user_tables(flask_request)

        # "user": user_table,
        # "tenants": tenants_table,
        # "shared_tenants": shared_tenants_table
        # self.access_levels








       
    
 

    

    
    





        



def update_product_requests_quota(flask_request: Request):
    
    q = Quota(
        tenant_id=flask_request.headers.get("TenantId"),
        auth_token=flask_request.headers.get("Authorization"),
        units=10,
        uploader_id="product_requests"
    )
    
    res, status_code = q.check_quota(1)
    if status_code == 200:
        return q.update_quota(1)
    
    return res, status_code
    
    
