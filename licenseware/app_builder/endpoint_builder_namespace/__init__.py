"""

Here we are creating the `endpoint_builder_namespace` that will be imported in `app_builder` along with the route creation functions from this package.

No other modules need to be here, routes are created dynamically with `EndpointBuilder` class.

"""

from flask_restx import Namespace

from licenseware.decorators.auth_decorators import authorization_check

endpoint_builder_namespace = Namespace(
    name="Endpoint Builder",
    description="Routes created with EndpointBuilder",
    path="/custom_endpoint",
    decorators=[authorization_check],
)
