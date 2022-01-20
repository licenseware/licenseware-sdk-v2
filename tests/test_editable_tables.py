import unittest

from marshmallow import Schema, fields, validate
from licenseware.editable_table import editable_tables_from_schemas
from licenseware.editable_table import metaspecs, EditableTable
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

        self.assertIsInstance(editable_tables, list)
        self.assertEqual(len(editable_tables), 1)

        self.assertIsInstance(editable_tables[0]["columns"], list)
        self.assertEqual(len(editable_tables[0]["columns"]), 4)


        cols = ['_id', 'device_name', 'number_of_processors', 'options']
        for i in editable_tables[0]["columns"]:
            self.assertIn(i['prop'], cols)

            if i['prop'] == 'options':
                self.assertEqual(i['type'], "enum")
                self.assertIsInstance(i['values'], list)
                self.assertEqual(len(i['values']), 3)
                self.assertIn("MOUNTED", i['values'])
                self.assertIn("OPEN", i['values'])
                self.assertIn("UNKNOWN", i['values'])

    def test_editable_class(self):

        editable_tables = [EditableTable(DeviceTableSchema).specs]
        log.warning(editable_tables)

        self.assertIsInstance(editable_tables, list)
        self.assertEqual(len(editable_tables), 1)

        self.assertIsInstance(editable_tables[0]["columns"], list)
        self.assertEqual(len(editable_tables[0]["columns"]), 4)


        cols = ['_id', 'device_name', 'number_of_processors', 'options']
        for i in editable_tables[0]["columns"]:
            self.assertIn(i['prop'], cols)

            if i['prop'] == 'options':
                self.assertEqual(i['type'], "enum")
                self.assertIsInstance(i['values'], list)
                self.assertEqual(len(i['values']), 3)
                self.assertIn("MOUNTED", i['values'])
                self.assertIn("OPEN", i['values'])
                self.assertIn("UNKNOWN", i['values'])