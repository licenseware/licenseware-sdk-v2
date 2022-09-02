"""

`FeatureBuilder` class can be used to instantiate plugins/add-ons with their own routes and quota.

Usage:

Features can be pre-created in the sdk in the features module, like bellow.
```py

from .feature_builder import FeatureBuilder

PRODUCT_REQUESTS = FeatureBuilder(
    name="Product Requests",
    description="Allow users request products by sending emails",
    access_levels=['admin'],
    monthly_quota=10
)

```
You can also create the feature in the commons/features module in the app.

```py

from licenseware.feature_builder.features import PRODUCT_REQUESTS # or from where you created the feature


App = AppBuilder(
    name = 'Plugins',
    description = '',
    flags = [flags.BETA]
)

# Attach the feature to the app so the routes will be generated automatically
App.register_feature(PRODUCT_REQUESTS)

```

On a get request to `/appid/features` you will get a json object like bellow:

```json

{
  "available_features": [
    {
      "app_id": "plugins",
      "name": "Product Requests",
      "description": "Allow users request products by sending emails",
      "access_levels": [
        "admin"
      ],
      "monthly_quota": 10,
      "activated": false,
      "feature_id": "product_requests_feature",
      "feature_path": "/product-requests"
    }
  ],
  "initialized_features": []
}

```

To activate/deactivate the feature:
- make a POST request to `/features/feature_path` with the payload `{"activated": true}` (to activate the feature/addon)
- make a POST request to `/features/feature_path` with the payload `{"activated": false}` (to deactivate the feature/addon) 


Another get request to `/features` path will show the following result:

```json
{
  "available_features": [
    {
      "app_id": "plugins",
      "name": "Product Requests",
      "description": "Allow users request products by sending emails",
      "access_levels": [
        "admin"
      ],
      "monthly_quota": 10,
      "activated": true,
      "feature_id": "product_requests_feature",
      "feature_path": "/product-requests"
    }
  ],
  "initialized_features": [
    {
      "name": "Product Requests",
      "tenant_id": "0be6c669-ab99-41e9-9d88-753a8fcc4cf8",
      "access_levels": [
        "admin"
      ],
      "app_id": "plugins",
      "description": "Allow users request products by sending emails",
      "feature_id": "product_requests_feature",
      "feature_path": "/product-requests",
      "monthly_quota": 10
    }
  ]
}
```

Now `initialized_features` is filled with the feature we activated.


To see more info about the feature we can make a GET request to `/features/feature_path`
The follwing result will be returned:

```json
{
  "name": "Product Requests",
  "tenant_id": "0be6c669-ab99-41e9-9d88-753a8fcc4cf8",
  "access_levels": [
    "admin"
  ],
  "activated": true,
  "app_id": "plugins",
  "description": "Allow users request products by sending emails",
  "feature_id": "product_requests_feature",
  "monthly_quota": 10
}
```

We've seen how to activate/deactivate features and see more info related to the feature.

We can also update quota for the feature. We just need the import the instantiated feature and call `update_quota` method.


Bellow it's a trimmed down example on how we can keep track of a feature usage.


```py

from flask import request
from flask_restx import Resource, Namespace, fields
from licenseware.mongodata import collection

from licenseware.feature_builder.features import PRODUCT_REQUESTS

ns = Namespace(
    name="Product requests controler",
    description="Send a request message to admins",
    path='/requests'

)

model = ns.model("model", dict(
    message_request = fields.String(required=True)
))


@ns.route("")
class ProductRequest(Resource):

    @ns.expect(model, validate=True)
    def post(self):

        response, status_code = PRODUCT_REQUESTS.update_quota(request, 1)
        
        if status_code != 200:
            return response, status_code
        
        with collection("Data") as col:
            col.insert_one(request.json)
    
        return "Request added", 200

```

Once the quota is being used another GET request to `/features/feature_path` will show more info about the quota.

```json
{
  "name": "Product Requests",
  "tenant_id": "0be6c669-ab99-41e9-9d88-753a8fcc4cf8",
  "access_levels": [
    "admin"
  ],
  "activated": true,
  "app_id": "plugins",
  "description": "Allow users request products by sending emails",
  "feature_id": "product_requests_feature",
  "monthly_quota": 10,
  "monthly_quota_consumed": 2,
  "quota_reset_date": "2022-03-16T08:18:20.713437"
}
```



"""


from typing import List

from flask import Request

from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.serializers import FeaturesSchema
from licenseware.quota import Quota
from licenseware.tenants.user_utils import current_user_has_access_level


class FeatureBuilder:
    def __init__(
        self,
        name: str,
        description: str = None,
        access_levels: List[str] = None,
        monthly_quota: int = 1,
        activated: bool = False,
        feature_id: str = None,
        feature_path: str = None,
    ):
        self.app_id = envs.APP_ID
        self.name = name
        self.description = description
        self.access_levels = access_levels
        self.monthly_quota = monthly_quota
        self.activated = activated
        self.feature_id = feature_id
        self.feature_path = feature_path

        self.get_details()

    def get_details(self):

        # ! There can't be 2 features with the same `name`
        # `decorators` will be applied on the route created
        # `access_levels` will be verified with auth
        #  Ex:
        #  access_levels = ['admin'] will check
        #  `shared_tenant` table `access_level` column for `admin` value
        #  or if user is the tenant owner

        if self.feature_id is None:
            self.feature_id = self.name.lower().replace(" ", "_") + "_feature"

        if self.feature_path is None:
            self.feature_path = "/" + self.feature_id.replace("_", "-").replace(
                "-feature", ""
            )

        return {
            "app_id": self.app_id,
            "name": self.name,
            "description": self.description,
            "access_levels": self.access_levels,
            "monthly_quota": self.monthly_quota,
            "activated": self.activated,
            "feature_id": self.feature_id,
            "feature_path": self.feature_path,
        }

    def feature_is_activated(self, tenant_id: str):

        feature_activated = mongodata.document_count(
            match={
                "tenant_id": tenant_id,
                "feature_id": self.feature_id,
                "activated": True,
            },
            collection=envs.MONGO_COLLECTION_FEATURES_NAME,
        )

        return True if feature_activated else False

    def update_quota(self, flask_request: Request, units: int = 1):

        tenant_id = flask_request.headers.get("TenantId")

        if not self.feature_is_activated(tenant_id):
            return "Feature is not activated. Can't update quota", 400

        q = Quota(
            tenant_id=tenant_id,
            auth_token=flask_request.headers.get("Authorization"),
            units=self.monthly_quota,
            uploader_id=self.feature_id,
        )

        res, status_code = q.check_quota(units)
        if status_code == 200:
            return q.update_quota(units)

        return res, status_code

    def get_status(self, flask_request: Request):

        tenant_id = flask_request.headers.get("TenantId")

        results = mongodata.fetch(
            match=(
                {"tenant_id": tenant_id, "name": self.name},
                {"_id": 0, "feature_path": 0},
            ),
            collection=envs.MONGO_COLLECTION_FEATURES_NAME,
        )

        if not results:
            return {}, 200

        quotas = mongodata.fetch(
            match=(
                {"tenant_id": tenant_id, "uploader_id": self.feature_id},
                {"_id": 0, "feature_path": 0},
            ),
            collection=envs.MONGO_COLLECTION_UTILIZATION_NAME,
        )

        if quotas:
            results[0]["monthly_quota_consumed"] = quotas[0]["monthly_quota_consumed"]
            results[0]["quota_reset_date"] = quotas[0]["quota_reset_date"]

        return results[0], 200

    def set_status(self, tenant_id: str, status: bool):

        self.activated = status
        feature_details = self.get_details()
        feature_details["tenant_id"] = tenant_id

        updated = mongodata.update(
            schema=FeaturesSchema,
            match={"tenant_id": tenant_id, "name": self.name},
            new_data=feature_details,
            collection=envs.MONGO_COLLECTION_FEATURES_NAME,
        )

        return updated

    def update_status(self, flask_request: Request):

        status = flask_request.json["activated"]
        tenant_id = flask_request.headers.get("TenantId")

        resp = f"Feature {'activated' if status else 'deactivated'}", 200

        if len(self.access_levels) == 0:
            self.set_status(tenant_id, status)
            return resp

        if current_user_has_access_level(flask_request, self.access_levels):
            self.set_status(tenant_id, status)
            return resp

        return "Not enough rights to activate/deactivate feature", 401
