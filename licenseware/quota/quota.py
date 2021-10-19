import sys
import datetime
import dateutil.parser as dateparser
from typing import Tuple
from dataclasses import dataclass

from marshmallow import Schema

from licenseware import mongodata
from licenseware.common.constants import envs, states
from licenseware.common.serializers import QuotaSchema
from licenseware.tenants.info import get_tenants_list, get_user_profile
from licenseware.utils.logger import log


@dataclass
class quota_plan:
    UNLIMITED:str = "UNLIMITED"
    FREE:str = "FREE" 


def get_quota_reset_date():
    quota_reset_date = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()



class Quota:
    
    def __init__(
        self,
        tenant_id:str,
        auth_token:str,
        uploader_id:str,
        units:int,
        schema:Schema = None,
        collection:str = None,
    ):
         
             
        self.units = units
        self.tenant_id = tenant_id
        self.uploader_id = uploader_id
        self.schema = schema or QuotaSchema
        self.collection = collection or envs.MONGO_COLLECTION_UTILIZATION_NAME
         
        self.tenants = get_tenants_list(tenant_id, auth_token)
        self.user_profile = get_user_profile(tenant_id, auth_token)
        
        self.plan_type = self.user_profile["plan_type"]
        
        # This is used to calculate quota
        self.user_query = {
            'tenant_id': { "$in": self.tenants },
            'uploader_id': uploader_id
        }
        
        # This is used to update quota
        self.tenant_query = {
            'tenant_id': tenant_id,
            'uploader_id': uploader_id
        }
        
        
        # Making sure email is verified
        if not self.user_profile["email_verified"]:
            raise Exception("Email not verified. Check your inbox for the activation link.")
        
        # Making sure quota is initialized
        response, status_code = self.init_quota()
        if status_code != 200:
            # will be cached in the api make sure to add @failsafe(failcode=500) decorator
            raise Exception(response['message']) 
    
    
    def get_monthly_quota(self):
        
        if self.plan_type == quota_plan.UNLIMITED:
            return sys.maxsize  
        
        if self.plan_type == quota_plan.FREE:
            return self.units 
        
        raise Exception(f"Can't determine `monthly_quota` based on plan_type: {self.plan_type}")
        
    
    def init_quota(self) -> Tuple[dict, int]:

        results = mongodata.fetch(
            match=self.tenant_query,
            collection=self.collection
        )

        if results:
            return {'status': states.SUCCESS, 'message': 'Quota initialized'}, 200
        
        utilization_data = {
            "tenant_id": self.tenant_id,
            "uploader_id": self.uploader_id,
            "monthly_quota": self.get_monthly_quota(),
            "monthly_quota_consumed": 0,
            "quota_reset_date": get_quota_reset_date()
        }

        inserted_ids = mongodata.insert(
            schema=self.schema, data=utilization_data, collection=self.collection
        )

        if isinstance(inserted_ids, list) and len(inserted_ids) == 1:
            return {'status': states.SUCCESS, 'message': 'Quota initialized'}, 200

        return {'status': states.FAILED, 'message': 'Quota failed to initialize'}, 500



    def update_quota(self, units:int) -> Tuple[dict, int]:
        
        current_utilization = mongodata.fetch(
            match=self.tenant_query,
            collection=self.collection
        )

        new_utilization = current_utilization[0]
        new_utilization['monthly_quota_consumed'] += units
        _id = new_utilization.pop('_id')
        
        updated_docs = mongodata.update(
            schema=self.schema,
            match={'_id': _id},
            new_data=new_utilization,
            collection=self.collection, 
            append=False
        )

        if updated_docs != 1:
            return {'status': states.FAILED, 'message': 'Quota update failed'}, 500
        
        return {'status': states.SUCCESS, 'message': 'Quota updated'}, 200

        
    def check_quota(self, units:int = 0) -> Tuple[dict, int]:

        results = mongodata.fetch(self.user_query, self.collection)
        
        # Reset quota if a month has passed 
        for quota in results:
            quota_reset_date = dateparser.parse(quota['quota_reset_date'])
            current_date = datetime.datetime.utcnow()
            if quota_reset_date < current_date:
                quota['quota_reset_date'] = get_quota_reset_date()
                quota['monthly_quota_consumed'] = 0
                _id = quota.pop('_id')
                mongodata.update(
                    schema=self.schema, 
                    match={'_id': _id}, 
                    new_data=quota, 
                    collection=self.collection
                )
                # Recall check_quota method with the new reseted date and quota
                self.check_quota(units)
            
            
        # Calculating quota consumed for this user_id
        monthly_quota_consumed = 0
        for quota in results:
            monthly_quota_consumed += quota['monthly_quota_consumed']
        
        if monthly_quota_consumed + units <= quota['monthly_quota']:
            return {
                        'status': states.SUCCESS,
                        'message': 'Utilization within monthly quota',
                        'monthly_quota': quota['monthly_quota'],
                        'quota_reset_date': quota['quota_reset_date']
                    }, 200
        else:
            return {
                        'status': states.FAILED,
                        'message': 'Monthly quota exceeded',
                        'monthly_quota': quota['monthly_quota'],
                        'quota_reset_date': quota['quota_reset_date']
                    }, 402


