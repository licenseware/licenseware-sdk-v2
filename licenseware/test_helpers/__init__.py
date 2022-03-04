"""

# Controllers (api declarations)

Here are some test helpers utilities which are useful in creating unit tests.

Ideally each controler should contain only funtionality related to swagger/openapi docs and 
each endpoint should call a function or class method which returns a response and a status code.

No business logic should be incorporated in the controller.

The `failsafe` decorator provided by the sdk should be placed ONLY on endpoints to prevent app crash.

Bellow is a recommendation on how the controller should look:

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

Create all needed `test_*.py` files in the `tests` folder next to the `app`.

Ex:
```bash
.
├── __init__.py
├── test_add_catalogs.py
└── test_merge_catalogs.py
```

Ideally you should test one feature per test case. For example up we have a test suite for adding catalogs
and one separate for merging catalogs.

Example of a test:

```py

import pytest
from unittest import TestCase
from flask.testing import Client
from licenseware.mongodata import collection
from licenseware.common.constants import envs
from licenseware.utils.logger import log

from main import app # this is used to get the flask test client and initialize app and workers
from app.common.constants import collections

from licenseware.test_helpers.auth import AuthHelper # this is useful to get authorization headers


# this will be used on all tests (in case of endpoint testing)
@pytest.fixture
def c():
    with app.test_client() as client:
        yield client



@pytest.fixture
def teardown():
    clean_db()



# some utilities functions specific to this test
def increase_quota():
    with collection(envs.MONGO_COLLECTION_UTILIZATION_NAME) as col:
        res = col.find_one(filter={'uploader_id': 'catalogs_quota'})
        if res is None: return
        if res['monthly_quota'] <= 1:
            col.update_one(
                filter={'uploader_id': 'catalogs_quota'},
                update={"$inc": {'monthly_quota': 9999}}
            )

# asserts can be used also instead of unittest.TestCase assertions
T = TestCase()


# some global variables used 
main_admin = "alin+mainadmin@licenseware.io"

catalog1 = "Catalog 1"
catalog2 = "Catalog 2"
catalog3 = "Catalog 3"
catalog4 = "Catalog 4"
cloned_lware_catalog = "Cloned Licenseware Catalog"

user_email1 = "alin+user1@licenseware.io"
user_email2 = "alin+user2@licenseware.io"
user_email3 = "alin+user3@licenseware.io"
user_email4 = "alin+user4@licenseware.io"

admin_email1 = "alin+admin1@licenseware.io"
admin_email2 = "alin+admin2@licenseware.io"
admin_email3 = "alin+admin3@licenseware.io"
admin_email4 = "alin+admin4@licenseware.io"


# tox tests/test_catalogs.py


# tox tests/test_catalogs.py::test_add_new_catalogs
def test_add_new_catalogs(c: Client):

    auth_headers = AuthHelper(main_admin).get_auth_headers()

    response = c.get(
        '/ssc/activate_app',
        headers=auth_headers
    )

    T.assertEqual(response.status_code, 200)

    increase_quota()

    catalogs = [
        {
            "catalog_name": catalog1,
            "tags": ["IT"],
            "admins": [main_admin, admin_email1],
            "users": [user_email1]
        },
        {
            "catalog_name": catalog2,
            "tags": ["IT"],
            "admins": [main_admin, admin_email2],
            "users": [user_email2]
        },
        {
            "catalog_name": catalog3,
            "tags": ["IT"],
            "admins": [main_admin, admin_email3],
            "users": [user_email3]
        }
    ]

    for payload in catalogs:
        response = c.post(
            '/ssc/catalogs',
            json=payload,
            headers=auth_headers
        )

        log.warning(response.data)
        # log.warning(response.get_json())

        T.assertEqual(response.status_code, 201)



def test_something_else(c: Client):

    result = get_somthing_from_db()
    assert admin_email3 in result



# etc

```

If tests are dependent on each other (data from a test is needed on another test) 
you can either place all tests in one file (big file hard to manage though) or
get add the seed data to db in a fixture function (recomended) 


"""
