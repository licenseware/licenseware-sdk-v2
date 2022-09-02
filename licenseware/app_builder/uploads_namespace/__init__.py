"""

Here we are creating the `uploads_namespace` that will be imported in `app_builder` along with the route creation functions from this package.

Use one module per route.

"""

from flask_restx import Namespace

from licenseware.common.constants import envs

# Here we are importing the route creation functions
# Each function will receive the `uploads_namespace` as a first parameter followed by other parameters if needed
from .filenames_validation_namespace import get_filenames_validation_namespace
from .filestream_validation_namespace import get_filestream_validation_namespace
from .quota_namespace import get_quota_namespace
from .status_namespace import get_status_namespace

# Here we are defining the uploads namespace which will be imported in app_builder
uploads_namespace = Namespace(
    name="File Uploads",
    description="Routes available for file processing operations",
    path=envs.UPLOAD_PATH,
)
