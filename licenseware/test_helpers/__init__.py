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

TODO

```py

TODO

```


"""
