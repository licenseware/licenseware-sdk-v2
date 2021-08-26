"""

Small 1 liners utilities that are to small to pe placed in a module 

"""

import random
import string
import requests
from flask_restx import Namespace
from marshmallow import Schema
from marshmallow_jsonschema import JSONSchema
from typing import List

from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs



def generate_id(length=6):
    """ Create a random series of digits of length specified """
    return "".join([random.choice(list(string.digits)) for _ in range(length)])


def flat_dict(li: List[dict]) -> dict:
    """ 
        - input_list = [{'width': 'full'}, {'height': '100vh'}]
        - output_dict = {'width': 'full', 'height': '100vh'}
    """
    return {k: v for dict_ in li for k, v in dict_.items()}  


def build_restx_model(ns: Namespace, schema: Schema, model_name:str = None):
    """ 
        Convert a marshmallow schema to a flask restx model 
        Resulted restx model can be used for swagger (body, marshal_with, expect, etc) 
    """
    
    model_name = model_name or schema.__name__
    
    json_schema = JSONSchema().dump(schema())["definitions"][schema.__name__]
    restx_model = ns.schema_model(model_name, json_schema) 
    
    return restx_model
    


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


swagger_authorization_header = {
    'Tenantid': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Tenantid'
    },
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


def get_user_id(tenant_id:str = None):
    
    response = requests.get(
        url=envs.AUTH_USERS_URL,
        headers={
            "TenantId": tenant_id,
            "Authorization": envs.get_auth_token()
        }
    )
    
    if response.status_code == 200:
        user_id = response.json()['user_id']
        return user_id
    