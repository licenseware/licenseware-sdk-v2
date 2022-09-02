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
from licenseware.common import marshmallow_to_restx_model
from app.services.catalogs import get_all_catalogs
from app.serializers import CatalogSchema

from app.utils.decorators import access_level
from app.common.constants import rights



ns = Namespace(
    name="Catalogs",
    description="Admin users can handle product catalogs. Regular users can view catalogs.",
    path='/catalogs',
    decorators=[authorization_check]
)


catalog_model = marshmallow_to_restx_model(ns, CatalogSchema)


@ns.route('')
class CrudApi(Resource):
    
    @failsafe(fail_code=500)
    @ns.doc(description="Get list of all saved catalogs")
    @ns.param('limit', 'Limit the number of results')
    @ns.param('skip', 'Skip the first n results')
    @ns.param('search_value', 'Search for a specific value')
    @ns.response(200, description="List of all saved catalogs", model=[catalog_model]) 
    @ns.response(406, description="Access for this catalog is forbidden", model=None) 
    @ns.response(500, description="Could not get catalogs. Something went wrong.", model=None) 
    def get(self):
        # Extract data from request (this would make it easier for unit-test the function)
        tenant_id = request.headers.get("TenantId)
        payload = request.json
        return get_all_catalogs(tenant_id, payload)
        
    # etc
    
    
```

The function `get_all_catalogs` contains the logic required.
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

TIP: this boilerplate can be created from terminal just by typing:
- `licenseware create-tests` (the stack manager and the service needs to be up and running)

```py
import pytest
from flask.testing import Client
from licenseware.common.constants import envs
from licenseware.test_helpers.auth import AuthHelper

from main import app

from . import clear_db, test_email, test_password


@pytest.fixture(scope="module")
def c():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def auth_headers():
    return AuthHelper(test_email, test_password).get_auth_headers()


# tox tests/test_*
# tox tests/test_product_requests_state_of_product_requests_plugin.py


# tox tests/test_product_requests_state_of_product_requests_plugin.py::test_product_requests_state_of_product_requests_plugin_get
def test_product_requests_state_of_product_requests_plugin_get(
    c: Client, auth_headers: dict
):
    \""" Returns the current state of the 'Product Request' plugin/feature \"""

    response = c.get(
        f"{envs.APP_PATH}/product-requests/state-of-product-requests-plugin",
        headers=auth_headers,
    )
    print("GET", response.data)
    assert response.status_code == 200
    clear_db()


```

If tests are dependent on each other (data from a test is needed on another test) 
you can either place all tests in one file (big file hard to manage though) or
get add the seed data to db in a fixture function (recomended) 


"""

from .auth import AuthHelper
