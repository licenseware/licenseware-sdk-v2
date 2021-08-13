import datetime
import os
import sys
import uuid
import dateutil.parser as dateparser
from marshmallow.schema import Schema
from app.licenseware.common.serializers import AppUtilizationSchema
from app.licenseware.common.constants import envs
from app.licenseware.utils.logger import log
import app.licenseware.mongodata as mongodata



# TODO 
# add QUOTA dict in the file validator ?
# or to constants or an endpoint?

#TODO
# add a `unit` per upload 
# ex: MDM "sccm_queries" we count 1 utilization for each 3 pack of csv files
# something like: get_sccm_queries_usage(3) == 1


QUOTA = {
    #IFMP
    "cpuq": 10,  # Databases
    "rv_tools": 1,  # Files
    "lms_detail": 1,  # Files
    "powercli": 1,  # Files
    
    #ODB
    "review_lite": 16, # Databases
    "lms_options": 1, # Files

    #OFMW
    "ofmw_archive": 1,  # 1 Device  == 1 archive
    
    #CM
    "pdf_contract": 1, # 1 pdf contract
    
    #MDM
    "sccm_queries": 1 # 1 pack of 3 csv files
}


if os.getenv('DEBUG') == 'true':
    QUOTA = dict(
        zip(QUOTA.keys(), [sys.maxsize]*len(QUOTA.keys()))
    )

    
# Utils

def get_quota_reset_date():
    quota_reset_date = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()



# TODO there is an issue with quota each time a new tenant is created quota is reseted 
# resulting in an unlimited use

# add a new endpoint to auth service with returns all tenants asociated with an user id
# calculate quota based on sum of tenants usage
# when a tenant/project is deleted from front-end 
# set tenant status to disabled in utilization collection 
# keep tenant utilization document until next reset quota



class Quota:

    def __init__(
        self, 
        tenant_id:str,
        uploader_id:str, 
        schema:Schema = None,
        collection:str = None 
    ):
        self.tenant_id = tenant_id
        self.uploader_id = uploader_id
        self.schema = schema or AppUtilizationSchema
        self.collection = collection or envs.MONGO_UTILIZATION_NAME
        self.query = {
            'tenant_id': self.tenant_id, 
            'uploader_id': self.uploader_id
        }


    def init_quota(self):

        results = mongodata.fetch(match=self.query, collection=self.collection)

        if results:
            return {'status': 'success', 'message': 'Quota already initialized'}, 200

        init_data = {
            "_id": str(uuid.uuid4()),
            "tenant_id": self.tenant_id,
            "uploader_id": self.uploader_id,
            "monthly_quota": QUOTA[self.uploader_id], #TODO get it somehow from the uploader validator class/function
            "monthly_quota_consumed": 0,
            "quota_reset_date": get_quota_reset_date()
        }

        inserted_ids = mongodata.insert(
            schema=self.schema, data=init_data, collection=self.collection
        )

        if not isinstance(inserted_ids, str):
            return {'status': 'success', 'message': 'Quota initialized'}, 201

        log.error(inserted_ids)
        
        return {'status': 'fail', 'message': 'Quota failed to initialize'}, 500



    def update_quota(self, number_of_units:int):
        
        current_utilization = mongodata.fetch(match=self.query, collection=self.collection)

        if current_utilization:
            new_utilization = current_utilization[0]
            new_utilization['monthly_quota_consumed'] += number_of_units
            
            updated_docs = mongodata.update(
                schema=self.schema,
                match=current_utilization[0],
                new_data=new_utilization,
                collection=self.collection, 
                append=False
            )

            if updated_docs == 1:
                return {'status': 'success', 'message': 'Quota updated'}, 200
            else:
                return {'status': 'fail', 'message': 'Quota failed to be updated'}, 500

        else:
            new_user_status, response = self.init_quota()
            if response == 200:
                retry_update = self.update_quota(number_of_units)
                return retry_update
            else:
                return new_user_status, response


    def check_quota(self, number_of_units:int = 0):

        results = mongodata.fetch(self.query, self.collection)

        if not results:
            new_user_response, status = self.init_quota()
            if status == 200:
                results = mongodata.fetch(self.query, self.collection)
                if results: quota = results[0]
            else:
                return new_user_response, status
        else:
            quota = results[0]


        # Reset quota if needed 
        quota_reset_date = dateparser.parse(quota['quota_reset_date'])
        current_date = datetime.datetime.utcnow()
        
        if quota_reset_date < current_date:
            quota['quota_reset_date'] = get_quota_reset_date()
            quota['monthly_quota_consumed'] = 0
            mongodata.update(
                schema=self.schema, 
                match=results[0], 
                new_data=quota, 
                collection=self.collection
            )
            
            # Recall check_quota method with the new reseted date and quota
            self.check_quota(number_of_units)


        if quota['monthly_quota_consumed'] <= quota['monthly_quota'] + number_of_units:
            return {
                        'status': 'success',
                        'message': 'Utilization within monthly quota'
                    }, 200
        else:
            return {
                        'status': 'fail',
                        'message': 'Monthly quota exceeded'
                    }, 402
