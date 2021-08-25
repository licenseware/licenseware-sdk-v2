"""

This module makes available the `namespace` decorator 
which can be used to generate flask_restx namespace from marshmallow schema

```py

from licenseware.decorators import namespace, login_required
from marshmallow import fields, Schema


class CatSchema(Schema):
	_id = fields.Integer(required=True)
	name = fields.String(required=True)


# Can be done in 2 ways

# 1. using the namespace decorator

@namespace(schema=CatSchema, collection='MongoCollectionName', decorators=[login_required])
class CatNamespace: 
	# overwrite get, post, put, delete methods
	...


# or  
# 2. Using the SchemaNamespace class with the defaults

DeviceNamespace = SchemaNamespace(
    schema=DeviceSchema, 
    collection='IFMPData', 
    methods=['GET', 'POST']
)


```

The example up provides all basic CRUD operations and swagger documentation.


If you decide to overwrite get, post, put, delete requests you can provide function parameters as query parameters.
You can retrive them with flask's `request.args`.
Query parameters MUST be set to None (ex: `def get(self, param1=None, param2=None): ...`)

Once your CRUD implementation is done you can import `CatNamespace` class in your namespace gatherer file:

```py

from flask import Blueprint
from flask_restx import Api

from .mymodule import CatNamespace

blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='My title', version='1.0')

api.add_namespace(CatNamespace(), path='/schema')

```

`CatNamespace()` will return the flask_restx namespace generated.

"""

from .schema_namespace import SchemaNamespace
