import unittest

from marshmallow import Schema, fields, validate
from licenseware.editable_table import editable_tables_from_schemas
from licenseware.editable_table import metaspecs
from licenseware.utils.logger import log


# python3 -m unittest tests/test_editable_tables.py


class DeviceTableSchema(Schema):
    
    _id = fields.Str(required=False)
    device_name = fields.Str(required=True)
    number_of_processors = fields.Int(required=False)
    options = fields.Str(
        required=False, 
        validate=validate.OneOf(["MOUNTED", "OPEN", "UNKNOWN"], error='Only "MOUNTED", "OPEN", "UNKNOWN" values are accepted'),
        metadata=metaspecs(editable=True, visible=True, type='enum')
    )
    

class TestEditableTables(unittest.TestCase):
    
    def test_editable_tables(self):
        
        editable_tables = editable_tables_from_schemas([DeviceTableSchema])
        
        log.warning(editable_tables)
        
        