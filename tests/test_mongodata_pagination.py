import unittest
import uuid

from marshmallow import Schema, fields

from licenseware import mongodata
from licenseware.utils.logger import log

# python3 -m unittest tests/test_mongodata_pagination.py


class UniqueSchema(Schema):
    unique = fields.Str(required=True)


class TestPagination(unittest.TestCase):
    def setUp(self):
        self.collection = "TestCollection"

    def tearDown(self):
        mongodata.delete_collection(self.collection)

    def test_mongodata_pagination(self):

        mongodata.insert(
            schema=UniqueSchema,
            collection=self.collection,
            data=[{"unique": str(uuid.uuid4())} for _ in range(80)],
        )

        document_counted = mongodata.document_count(
            match={}, collection=self.collection
        )

        log.warning(f"Number of documents: {document_counted}")

        # Using __pagination__ match field

        currently_fetched_items = 0

        results = mongodata.fetch(
            match={
                "__pagination__": {
                    "max_items_to_fetch": 20,
                    "currently_fetched_items": currently_fetched_items,
                }
            },
            collection=self.collection,
        )

        self.assertEqual(len(results), 20)
        currently_fetched_items += len(results)

        first_batch = results[-1]

        results = mongodata.fetch(
            match={
                "__pagination__": {
                    "max_items_to_fetch": 20,
                    "currently_fetched_items": currently_fetched_items,
                }
            },
            collection=self.collection,
        )

        self.assertEqual(len(results), 20)
        currently_fetched_items += len(results)

        second_batch = results[-1]

        self.assertNotEqual(first_batch["unique"], second_batch["unique"])

        # Using limit/skip

        results = mongodata.fetch(
            match={}, limit=20, skip=currently_fetched_items, collection=self.collection
        )

        self.assertEqual(len(results), 20)
        currently_fetched_items += len(results)

        third_batch = results[-1]

        results = mongodata.fetch(
            match={}, limit=20, skip=currently_fetched_items, collection=self.collection
        )

        self.assertEqual(len(results), 20)
        currently_fetched_items += len(results)

        fourth_batch = results[-1]

        self.assertNotEqual(third_batch["unique"], fourth_batch["unique"])
