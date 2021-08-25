import random
import string
from flask_restx import Namespace
from marshmallow import Schema
from marshmallow_jsonschema import JSONSchema
from typing import List



swagger_authorization_header = {
    'TenantId': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'TenantId'
    },
    'Authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


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
    
