import requests
from licenseware.common.constants import envs



def get_tenants_list(tenant_id:str, auth_token:str):

    response = requests.get(
        url=envs.AUTH_TENANTS_URL,
        headers={
            "Tenantid": tenant_id,
            "Authorization": auth_token
        }
    )
    
    if response.status_code == 200:
        data_list = response.json()['data']
        tenants_list = [data['id'] for data in data_list]
        return tenants_list
    


def get_user_profile(tenant_id:str, auth_token:str):

    response = requests.get(
        url=envs.AUTH_USER_PROFILE_URL,
        headers={
            "Tenantid": tenant_id,
            "Authorization": auth_token
        }
    )
    
    if response.status_code == 200:
        return response.json()
        # "id": user_id,
        # "email": 'user.email',
        # "first_name": 'user.first_name',
        # "last_name": 'user.last_name',
        # "company_name": 'user.company_name',
        # "job_title": 'user.job_title',
        # "plan_type": 'user.plan_type',
        # "email_verified": 'user.email_verified',
        # "profile_pic": 'user.profile_pic'
        