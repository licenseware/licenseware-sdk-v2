"""

# Controllers (api declarations)

Here are some test helpers utilities which are useful in creating unit tests.

Ideally each controler should contain only funtionality related to swagger/openapi docs and 
each endpoint should call a function or class method which returns a response and a status code.

No business logic should be incorporated in the controller.

The `failsafe` decorator provided by the sdk should be placed ONLY on endpoints to prevent app crash.

Bellow is a recomandation on how the controller should look: 

```py
# /app/controlers/catalogs_controller.py

from flask import request
from flask_restx import Resource, Namespace, fields
from licenseware.decorators.failsafe_decorator import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.utils.logger import log

from app.services.catalogs import get_all_catalogs
    

from app.utils.decorators import access_level
from app.common.constants import rights



ns = Namespace(
    name="Catalogs",
    description="Admin users can handle product catalogs. Regular users can view catalogs.",
    path='/catalogs',
    decorators=[authorization_check]
)


catalog_model = ns.model("new_catalog", dict(    
    catalog_name = fields.String(required=True, description='Catalog name'),
    tags = fields.List(fields.String, description='List of tags/categories which this catalog belongs to'),
    admins = fields.List(fields.String, required=True, description='List of admins for this catalog (emails)'),
    users = fields.List(fields.String, required=False, description='List of users for this catalog (emails)')
))


catalog_model_list = ns.clone("catalogs_list", catalog_model, dict(
    updated_at = fields.String(required=False),
    catalog_id = fields.String(required=False),
    product_requests_allowed = fields.Boolean(required=False),
    number_of_products = fields.Integer()
))


@ns.route('')
class CrudApi(Resource):
    
    @failsafe(fail_code=500)
    @ns.doc(description="Get list of all saved catalogs")
    @ns.param('limit', 'Limit the number of results')
    @ns.param('skip', 'Skip the first n results')
    @ns.param('search_value', 'Search for a specific value')
    @ns.response(200, description="List of all saved catalogs", model=[catalog_model_list]) 
    @ns.response(406, description="Access for this catalog is forbidden", model=None) 
    @ns.response(500, description="Could not get catalogs. Something went wrong.", model=None) 
    def get(self):
        return get_all_catalogs(request)
        
    # etc
    
    
```

The function `get_all_catalogs` contains the logic required 
to process the flask request received or other parameters/path parameters provided.

Function `get_all_catalogs` will return a response and a status_code.


# Test creation

Next to `app` module create if not found a `tests` folder. 

Inside tests folder create a module for each controller from `app/controllers`.

Ex:

The controler described up can be found in `/app/controlers/catalogs_controller.py`.
The test module name will be: `tests/test_1_catalogs.py`


> In most cases the tests will need to be executed in a specific order, notice the `test_1` naming.

In `tests/test_1_catalogs.py` add the following:


```py

from unittest import TestCase
from licenseware.test_helpers import get_auth_headers, get_flask_request, EMAIL            

from app.common.constants import collections
from app.services.catalogs import get_all_catalogs
  
from main import app
from licenseware import mongodata
from licenseware.utils.logger import log

t = TestCase() # this will be our assertion library


# Before tests we are writing some functionality which will be used in all tests (similar to setUp from unittest module)

def raise_quota_limit():    
    # Raise quota limits for tests
    with collection(envs.MONGO_COLLECTION_UTILIZATION_NAME) as col:
        res = col.find_one(filter={'uploader_id': 'catalogs_quota'})
        if res['monthly_quota'] <= 1:
            col.update_one(
                filter={'uploader_id': 'catalogs_quota'},
                update={"$inc": {'monthly_quota': 9999}}
            )




def delete_all_collections():
    
    mongodata.delete_collection(envs.MONGO_COLLECTION_ANALYSIS_NAME)
    mongodata.delete_collection(envs.MONGO_COLLECTION_DATA_NAME)
    mongodata.delete_collection(envs.MONGO_COLLECTION_UTILIZATION_NAME)
    mongodata.delete_collection(collections.CATALOGS)
    mongodata.delete_collection(collections.PRODUCT_REQUESTS)
    mongodata.delete_collection(collections.PRODUCTS)
    mongodata.delete_collection(collections.USERS)
    mongodata.delete_collection(collections.SETTINGS)

    load_licenseware_products_catalog()

        

catalog1 = "Catalog 1"
catalog2 = "Catalog 2"
catalog3 = "Catalog 3"
cloned_licenseware_catalog = "Cloned Licenseware Catalog"


auth_main_headers = get_auth_headers() # here we are getting credentials from envs (you could also provide them as parameters)

# Creating some mock users

user_email = "alin+user@licenseware.io"
user_email1 = "alin+user1@licenseware.io"
user_email2 = "alin+user2@licenseware.io"

admin_email = "alin+admin@licenseware.io"
admin_email1 = "alin+admin1@licenseware.io"
admin_email2 = "alin+admin2@licenseware.io"



# HELPERS

def get_catalog_by_name(catalog_name:str):

    catalogs = mongodata.fetch(
        match={'catalog_name': catalog_name},
        collection=collections.CATALOGS
    )
    
    t.assertIsInstance(catalogs, list)
    t.assertEqual(len(catalogs), 1)

    return catalogs[0]


# TESTS

def test_add_new_catalog():
    
    delete_all_collections()
            
    # First catalog
    payload = {
        "catalog_name": catalog1,
        "tags": ["IT"],
        "admins": [EMAIL, admin_email],
        "users": [user_email]
    }

    request = get_flask_request(
        headers=auth_main_headers,
        json=payload
    )
    
    decorators.request = request
    access = decorators.access_level(lambda: True, rights.CAN_ADD_CATALOG)()
    t.assertIsInstance(access, bool)
    t.assertEqual(access, True)

    response, status_code = add_new_catalog(request)
    
    t.assertEqual(status_code, 201)
    t.assertEqual(response['catalog_name'], payload['catalog_name'])

    catalog = get_catalog_by_name(catalog1)

    catalog_users = mongodata.fetch(
        match={'catalog_id': catalog['catalog_id']},
        collection=collections.USERS
    )

    t.assertEqual(len(catalog_users), 3)

    raise_quota_limit()
    

    # Second
    payload = {
        "catalog_name": catalog2,
        "tags": ["IT"],
        "admins": [EMAIL, admin_email1],
        "users": [user_email1]
    }
    
    request = get_flask_request(
        headers=auth_main_headers,
        json=payload
    )
    
    response, status_code = add_new_catalog(request)
    
    t.assertEqual(status_code, 201)
    t.assertEqual(response['catalog_name'], payload['catalog_name'])
    

    catalog = get_catalog_by_name(catalog2)
    
    catalog_users = mongodata.fetch(
        match={'catalog_id': catalog['catalog_id']},
        collection=collections.USERS
    )

    t.assertEqual(len(catalog_users), 3)


    # Third
    payload = {
        "catalog_name": catalog3,
        "tags": ["IT"],
        "admins": [EMAIL],
        "users": []
    }
    
    request = get_flask_request(
        headers=auth_main_headers,
        json=payload
    )
    
    response, status_code = add_new_catalog(request)
    
    t.assertEqual(status_code, 201)
    t.assertEqual(response['catalog_name'], payload['catalog_name'])
    

    catalog = get_catalog_by_name(catalog3)

    catalog_users = mongodata.fetch(
        match={'catalog_id': catalog['catalog_id']},
        collection=collections.USERS
    )

    t.assertEqual(len(catalog_users), 1)



```

The tests will run in the order they are placed in the file.


The function `get_auth_headers` depends on 2 environment variables:
- 'TEST_USER_EMAIL'
- 'TEST_USER_PASSWORD'
If they are not provided you will need to provide them in the `get_auth_headers` function.


Package `test_helpers` from sdk provides 2 useful functions which can be used for tests.

- `get_auth_headers` - given email, password and a optional tenant_id will register user to auth service and return auth headers.
- `get_flask_request`- filling the needed parameters will return an equivalent flask request which can be passed to functions from controllers 



"""




from .authentification import get_auth_headers, EMAIL, create_user, login_user, get_auth_tables
from .flask_request import get_flask_request
from .order_tests import load_ordered_tests