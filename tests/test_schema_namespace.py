import unittest

from main import app
from marshmallow import Schema, fields

from licenseware.common.constants import envs
from licenseware.schema_namespace import SchemaNamespace

# python3 -m unittest tests/test_schema_namespace.py


class TestNamespaceGenerator(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_schema_namespace(self):
        class UserSchema(Schema):
            class Meta:
                collection_name = envs.MONGO_COLLECTION_DATA_NAME

            name = fields.Str(required=True)
            occupation = fields.Str(required=True)

        UserNs = SchemaNamespace(schema=UserSchema, collection="TestCol", decorators=[])

        ns = UserNs.initialize()

        self.assertEqual(len(ns.resources), 1)
        self.assertEqual(
            sorted(ns.resources[0].resource.methods),
            sorted({"DELETE", "PUT", "POST", "GET"}),
        )
