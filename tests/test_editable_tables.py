import unittest

from marshmallow import Schema, fields
from licenseware import mongodata
from licenseware.editable_table import editable_tables_from_schemas
from licenseware.utils.logger import log


# python3 -m unittest tests/test_editable_tables.py


class DeviceTableSchema(Schema):
    _id = fields.Str(required=False)
    device_name = fields.Str(required=True)
    number_of_processors = fields.Int(required=False)
    

class TestEditableTables(unittest.TestCase):
    
    def test_editable_tables(self):
        
        editable_tables = editable_tables_from_schemas([DeviceTableSchema])
        
        log.warning(editable_tables)
        
        