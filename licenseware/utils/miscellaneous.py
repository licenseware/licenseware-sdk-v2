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

from licenseware.utils.logger import log



def generate_id(length=6):
    """ Create a random series of digits of length specified """
    return "".join([random.choice(list(string.digits)) for _ in range(length)])


def flat_dict(li: List[dict]) -> dict:
    """ 
        - input_list = [{'width': 'full'}, {'height': '100vh'}]
        - output_dict = {'width': 'full', 'height': '100vh'}
    """
    return {k: v for dict_ in li for k, v in dict_.items()}  


def get_json_schema(schema: Schema):
    """
        Generate json schema from marshmallow schema class
    """
    
    json_schema = JSONSchema().dump(schema())["definitions"][schema.__name__]
    
    return json_schema


def build_restx_model(ns: Namespace, schema: Schema, model_name:str = None):
    """ 
        Convert a marshmallow schema to a flask restx model 
        Resulted restx model can be used for swagger (body, marshal_with, expect, etc) 
    """
    
    model_name = model_name or schema.__name__
    
    json_schema = get_json_schema(schema)
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


def get_tenants_list(tenant_id:str, auth_token:str):

    from licenseware.common.constants import envs

    response = requests.get(
        url=envs.GET_TENANTS_URL,
        headers={
            "Tenantid": tenant_id,
            "Authorization": auth_token
        }
    )
    
    if response.status_code == 200:
        data_list = response.json()['data']
        tenants_list = [data['id'] for data in data_list]
        return tenants_list
    