"""

Here we are creating the `features_namespace` that will be imported in `app_builder` along with the route creation functions from this package.

Use one module per route.

"""

from flask_restx import Namespace

from licenseware.common.constants import envs

# Here we are importing the route creation functions
# Each function will receive the `features_namespace` as a first parameter followed by other parameters if needed
from .features_namespace import get_features_namespace

# Here we are defining the features namespace which will be imported in app_builder
features_namespace = Namespace(
    name="Features", description="Routes available for features", path=envs.FEATURE_PATH
)
