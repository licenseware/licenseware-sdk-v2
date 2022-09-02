import unittest

from marshmallow import Schema, fields, validate

from licenseware.editable_table import (
    EditableTable,
    editable_tables_from_schemas,
    metaspecs,
)
from licenseware.utils.logger import log

# python3 -m unittest tests/test_editable_tables.py


class DeviceTableSchema(Schema):

    _id = fields.Str(required=False)
    device_name = fields.Str(required=True)
    number_of_processors = fields.Int(required=False)
    options = fields.Str(
        required=False,
        validate=validate.OneOf(
            ["MOUNTED", "OPEN", "UNKNOWN"],
            error='Only "MOUNTED", "OPEN", "UNKNOWN" values are accepted',
        ),
        metadata=metaspecs(editable=True, visible=True, type="enum"),
    )

    device_type = fields.Str(
        required=True,
        validate=[
            validate.OneOf(
                ["Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"],
                error='Only allowed values are "Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"',
            )
        ],
        metadata={"editable": True, "visible": True},
    )


class TestEditableTables(unittest.TestCase):
    def test_editable_tables(self):

        editable_tables = editable_tables_from_schemas([DeviceTableSchema])
        log.warning(editable_tables)

        self.assertIsInstance(editable_tables, list)
        self.assertEqual(len(editable_tables), 1)

        self.assertIsInstance(editable_tables[0]["columns"], list)
        self.assertEqual(len(editable_tables[0]["columns"]), 5)

        cols = ["_id", "device_name", "number_of_processors", "options", "device_type"]
        for i in editable_tables[0]["columns"]:
            self.assertIn(i["prop"], cols)

            if i["prop"] == "options":
                self.assertEqual(i["type"], "enum")
                self.assertIsInstance(i["values"], list)
                self.assertEqual(len(i["values"]), 3)
                self.assertIn("MOUNTED", i["values"])
                self.assertIn("OPEN", i["values"])
                self.assertIn("UNKNOWN", i["values"])

    def test_editable_class(self):

        editable_tables = [EditableTable(DeviceTableSchema).specs]
        log.warning(editable_tables)

        self.assertIsInstance(editable_tables, list)
        self.assertEqual(len(editable_tables), 1)

        self.assertIsInstance(editable_tables[0]["columns"], list)
        self.assertEqual(len(editable_tables[0]["columns"]), 5)

        cols = ["_id", "device_name", "number_of_processors", "options", "device_type"]
        for i in editable_tables[0]["columns"]:
            self.assertIn(i["prop"], cols)

            if i["prop"] == "options":
                self.assertEqual(i["type"], "enum")
                self.assertIsInstance(i["values"], list)
                self.assertEqual(len(i["values"]), 3)
                self.assertIn("MOUNTED", i["values"])
                self.assertIn("OPEN", i["values"])
                self.assertIn("UNKNOWN", i["values"])
