import unittest

from licenseware.utils.logger import log
from marshmallow import Schema, fields

from licenseware.common.constants import envs
from licenseware.mongodata.mongo_connection import db
from licenseware import mongodata as m


# python3 -m unittest tests/test_mongodata.py

collection_name = 'TEST' + envs.MONGO_COLLECTION_DATA_NAME


class TestMongoData(unittest.TestCase):
    
    def test_simple_insert_one(self):
        
        doc = {
            'name': 'John',
            'occupation': 'dev'
        }
        
        data_collection = db[envs.MONGO_COLLECTION_DATA_NAME]
        
        response = data_collection.insert_one(doc)
        
        query = {'_id': response.inserted_id}
        
        response = data_collection.find_one(query)
        data = dict(response)
        
        self.assertEqual(data['name'], 'John')
        self.assertEqual(data['occupation'], 'dev')
        
        response = data_collection.delete_one(query)
        
        self.assertEqual(response.deleted_count, 1)
        
        
        
    def test_mongodata_insert(self):
        
        class MySchema(Schema):
            name = fields.Str(required=True)
            occupation = fields.Str(required=True)
            
        doc = {
            'name': 'John',
            'occupation': 'dev'
        }
        
        response = m.insert(
            schema=MySchema, 
            data=doc,
            collection=collection_name
        )
        
        self.assertEqual(len(response), 1)
        
        query = {'_id': response[0]}
        
        response = m.fetch(
            match=query,
            collection=collection_name
        )
        
        # log.debug(response)
        
        self.assertEqual(len(response), 1)
        
        data = response[0]
        
        self.assertEqual(data['name'], 'John')
        self.assertEqual(data['occupation'], 'dev')
        
        
    def test_insert_many(self):
        
        class MySchema(Schema):
            name = fields.Str(required=True)
            occupation = fields.Str(required=True)
            
        doclist = [
            {
                'name': 'John',
                'occupation': 'dev'
            },
            {
                'name': 'Steve',
                'occupation': 'dev'
            },
            {
                'name': 'Bob',
                'occupation': 'dev'
            },
            {
                'name': 'Jim',
                'occupation': 'dev'
            },
        ]
        
        inserted_id_list = m.insert(
            schema=MySchema, 
            data=doclist,
            collection=collection_name
        )
        
        self.assertEqual(len(inserted_id_list), len(doclist))
        
        for inserted_id in inserted_id_list:
            
            response = m.fetch(
                match={'_id': inserted_id},
                collection=collection_name
            )
            
            name_added = False
            for doc in doclist:
                if response[0]['name'] == doc['name']:
                    name_added = True
                    
            self.assertTrue(name_added)
                
            
    def test_update(self):
    
        class MySchema(Schema):
            name = fields.Str(required=False)
            occupation = fields.Str(required=True)
        
        doc = {
            'name': 'John',
            'occupation': 'copywriter'
        }
        
        response = m.insert(
            schema=MySchema, 
            data=doc,
            collection=collection_name
        )
        
        self.assertEqual(len(response), 1)
        
        updated_docs = m.update(
            schema=MySchema,
            match={'occupation': 'copywriter'},
            new_data={'occupation': 'developer'},
            collection=collection_name
        )
        
        self.assertEqual(updated_docs, 1)
        
        
        response = m.fetch(
            match={},
            collection=collection_name
        )
        
        self.assertTrue(len(response) > 1)








"""


def test_update_list_with_append():
    
    catalogdict = {
        'product_catalog_id': 'internet_application_server_standard',
        'product_name': 'Internet Application Server Standard',
        'result': 'Used',
        'tenant_id': '2ac111c7-fd19-463e-96c2-1493aea18bed',
        'version': '',
        'install_location': '',
        'product_category': 'Application Server Products',
        '_id': '57077fca-daae-582d-8335-8f413876c140',
    }

    data_list = [
        # {
        #     "name": "Dan lupin",
        #     "some_field": "this should remain unchanged"
        # },

        {
            # "_id": "append_test",
            "name": 'Alin',
            "some_field": "this should remain unchanged",
            "test_list": ["initial_list_value"], 
            "test_list2": [ "initial_list_value2"],
            "test_dict": {"initial_dict_key":"initial_dict_value"},
            "test_list_of_dict": [
                {"initial_dict_key":"initial_dict_value", "some_id":"1"},
                catalogdict
            ],
        }
    ]

    id_list = m.insert(AnotherDummySchema, "TestCollection", data_list)
    assert_that(len(id_list)).is_equal_to(len(data_list))
    
    # print(id_list)
    
    #Trying to see if duplicates from new_date are removed
    new_data = {
        "_id": id_list[0],
        'name': 'Alin', 
        "test_list": ["initial_list_value", "appended_value"],
        "test_list2": ['initial_list_value2', "appended_value2"],
        "test_dict": {"initial_dict_key":"initial_dict_value", "new_dict_key":"new_dict_value"},
        "test_list_of_dict": [
            {"initial_dict_key":"initial_dict_value", "some_id":"1"},
            {"new_dict_key":"new_dict_value"}, 
            catalogdict
        ]
    }


    # Updating the same data twice
    
    updated_data = m.update(
        schema     = AnotherDummySchema,
        collection ="TestCollection",
        match      = {"_id": id_list[0]},
        new_data   = new_data,
        append     = True
    )
    
    
    new_data = {
        "name": 'John',
        "test_list_of_dict": [
            {"initial_dict_key":"initial_dict_value", "some_id":"1"},
            {"new_dict_key":"new_dict_value"}, 
            sort_dict(catalogdict)
        ]
    }
     
    updated_data = m.update(
        schema     = AnotherDummySchema,
        collection ="TestCollection",
        match      = {"_id": id_list[0]},
        new_data   = new_data,
        append     = True
    )

    # print(updated_data)

    data = m.fetch(
        match = {"_id": id_list[0]},
        collection="TestCollection",
    )
    
    # print(data)

    dict_ = data[0]

    assert_that(dict_['test_list']).is_length(2)
    assert_that(dict_['test_list2']).is_length(2)
    assert_that(dict_['test_dict'].keys()).is_length(2)
    #TODO this fails (list of docs with $addToSet doesn't work)
    # assert_that(dict_['test_list_of_dict']).is_length(3)





    




def test_update_new_doc():
    
    new_data = {
        "_id": existing_id,
        "name": "radu"
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="TestCollection",
        match      = new_data["_id"],
        new_data   = new_data,
        append     = True
    )


    data = m.fetch(
        match = new_data["_id"],
        collection="TestCollection",
    )

    # print(data)

    assert_that(data).is_equal_to(new_data)
    


def test_update_new_doc_existing_id():
    
    new_data = {
        "_id": existing_id,
        "name": "cornelia"
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="TestCollection",
        match      = new_data["_id"],
        new_data   = new_data,
        append     = True
    )


    data = m.fetch(
        match = new_data["_id"],
        collection="TestCollection",
    )

    assert_that(data).is_equal_to(new_data)



def test_existing_id():
    test_update_new_doc()
    test_update_new_doc_existing_id()


def test_update_id_field_match():

    new_data = {
        "_id": existing_id,
        "name": "razvan",
        "test_list": ["data"]
    }

    updated_data = m.update(
        schema = AnotherDummySchema,
        collection="TestCollection",
        match      = {"_id": existing_id,"name": "cornelia"},
        new_data   = new_data,
        append     = True
    )

    data = m.fetch(
        match = new_data["_id"],
        collection="TestCollection",
    )

    # print(data)

    assert_that(data['_id']).is_equal_to(new_data["_id"])



def test_update_one_with_id():

    response = m.update(
        schema= AnotherDummySchema,
        collection = "TestCollection",
        match      = id1,
        new_data   = {'name': 'New John Show'},
        append     = True
    )
    
    #print(response)

    assert_that(response).is_equal_to(1)



def test_update_all_with_match():
    
    import re
    regx = re.compile("^New John", re.IGNORECASE)

    response = m.update(
        schema= AnotherDummySchema,
        collection = "TestCollection",
        match      = {'name': regx},
        new_data   = {'name': 'John'},
        append     = True
    )

    #print(response)

    assert_that(response).is_greater_than_or_equal_to(1)



def test_update_with_pullall():

    _id = str(uuid.uuid4())

    data = {
        "_id": _id,
        "name": "licenseware",
        "test_list": [1,2,3],
        "test_dict": {"nbr":2},
        "test_list_of_dict": [
            {"file_id": "should be unique", "other_data": "some data"},
            {"file_id": "thefileid", "other_data": "some data"}
        ]
    }

    inserted = m.insert(AnotherDummySchema, "TestCollection", data)

    assert_that(inserted).contains_only(_id)

    new_data = {
        "_id": _id,
        "name": "licenseware_new",
        "test_list_of_dict": [
            {"file_id": "should be unique", "other_data": "changed a little"},
        ]
    }


    m.update(
        AnotherDummySchema,
        match=_id,
        new_data=new_data,
        collection="TestCollection",
        append     = True
    )

    saved_data = m.fetch(_id, "TestCollection")

    # print(saved_data)












def test_fetch_with_agreggate():

    doc_list = m.aggregate(
        collection = "TestCollection",
        pipeline   = [{ "$match": {'name': 'John'} }],
        as_list = True        
    )

    # print(doc_list)

    assert_that(doc_list).is_instance_of(list).is_not_empty()


def test_fetch_distinct():

    doc_list = m.fetch(
        match = 'name',
        collection = "TestCollection",
        as_list = True        
    )

    # print(doc_list)

    assert_that(doc_list).is_instance_of(list).is_not_empty()



def test_delete_by_id():

    deleted_docs_nbr = m.delete(
        collection = "TestCollection",
        match      = id1,
    )

    #print(deleted_docs_nbr)

    assert_that(deleted_docs_nbr).is_equal_to(1)



def test_delete_with_query():

    deleted_docs_nbr = m.delete(
        collection = "TestCollection",
        match      = {'name': 'John'},
    )

    #print(deleted_docs_nbr)

    assert_that(deleted_docs_nbr).is_greater_than_or_equal_to(1)



def test_delete_collection():

    deleted_col_nbr = m.delete_collection(collection="TestCollection")

    # print(deleted_col_nbr)

    assert_that(deleted_col_nbr).is_equal_to(1)


"""
