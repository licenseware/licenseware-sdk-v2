"""

Here we are creating the `decrypt_namespace` that will be imported in `app_builder` along with the route creation functions from this package.

Use one module per route.

"""

from flask_restx import Namespace

# Here we are importing the route creation functions
# Each function will receive the `decrypt_namespace` as a first parameter followed by other parameters if needed
from .decrypt_namespace import get_decrypt_namespace

# from licenseware.common.constants import envs


# Here we are defining the decrypt namespace which will be imported in app_builder
decrypt_namespace = Namespace(
    name="Decrypt", description="Decrypt list of values received", path="/decrypt"
)
