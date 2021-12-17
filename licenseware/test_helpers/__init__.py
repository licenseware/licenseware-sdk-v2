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


In most cases the tests will need to be executed in a specific order, notice the `test_1` naming.

In `tests/test_1_catalogs.py` add the following:

```py

import unittest
from licenseware.test_helpers import (
    create_mock_flask_request,
    load_ordered_tests,
    get_auth_headers,
    EMAIL            
)




from app.common.constants import collections
from app.services.catalogs import get_all_catalogs
  
from main import app

from licenseware import mongodata
from licenseware.utils.logger import log



load_tests = load_ordered_tests


# python3 -m unittest tests/test_1_catalogs.py


class Test1Catalogs(unittest.TestCase):
    
    def setUp(self):
        mongodata.delete_collection("SSCQuota")
        self.auth_headers = get_auth_headers()
        self.catalog_name = "My Catalog"
        self.cloned_licenseware_catalog = "Cloned Licenseware Catalog"
        self.cloned_catalog = ""
        

    def test_get_all_catalogs(self):
        
        request = create_mock_flask_request(
            headers=self.auth_headers
        )
        
        response, status_code = get_all_catalogs(request)
        
        self.assertEqual(status_code, 200)
        self.assertIsInstance(response, list)
        self.assertGreaterEqual(len(response), 1)
        

```

Notice that the test class is named `Test1Catalogs`, 1 is for executing tests in order.

Inside test class `Test1Catalogs` the tests will be executed in the order they are placed in the class
because of the `load_tests = load_ordered_tests` line.


Notice that we are not using the `test_client` from flask.
We still need to import the flask `app` object from our `main.py` file.
 

Instead of the `test_client` we are building the request using `create_mock_flask_request` function from test_helpers.

In `create_mock_flask_request` function you can specify as parameters (dict) headers, json, args, TODO files.
 

The function `get_auth_headers` depends on 2 environment variables:
- 'TEST_USER_EMAIL'
- 'TEST_USER_PASSWORD'

These environment variables will be used to get the `Authorization` and `TenantId` value from `auth-service`.

TODO - create a test email which requires no email validation



"""




from .authentification import get_auth_headers, EMAIL
from .flask_request import create_mock_flask_request
from .order_tests import load_ordered_tests