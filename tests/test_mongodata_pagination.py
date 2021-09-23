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
        self.collection = 'TestCollection'

    def tearDown(self):
        mongodata.delete_collection(self.collection)
       
    def test_mongodata_pagination(self):
        
        mongodata.insert(
            schema=UniqueSchema,
            collection=self.collection,
            data=[ { 'unique': str(uuid.uuid4()) } for _ in range(80) ]
        )
        
        
        document_counted = mongodata.document_count(
            match={},
            collection=self.collection
        )
        
        log.warning(f"Number of documents: {document_counted}")        

        results = mongodata.fetch(
            match={
                    "#pagination": {
                        "max_items_to_fetch": 20,
                        "currently_fetched_items": 0
                    }
                },
            collection=self.collection
        )
        
        self.assertEqual(len(results), 20)
        
        first_batch = results[-1]
        
        
        results = mongodata.fetch(
            match={
                    "#pagination": {
                        "max_items_to_fetch": 20,
                        "currently_fetched_items": len(results)
                    }
                },
            collection=self.collection
        )
        
        self.assertEqual(len(results), 20)
        
        second_batch = results[-1]
        
        self.assertNotEqual(first_batch['unique'], second_batch['unique'])
        
        
        