"""

Here we are creating the `reports_namespace` that will be imported in `app_builder` along with the route creation functions from this package.

Use one module per route.

"""

from flask_restx import Namespace

from licenseware.common.constants import envs

from .report_components_namespace import get_report_components_namespace
from .report_image_preview_dark_namespace import get_report_image_preview_dark_namespace
from .report_image_preview_namespace import get_report_image_preview_namespace
from .report_metadata_namespace import get_report_metadata_namespace
from .report_public_components_namespace import get_public_report_components_namespace
from .report_public_metadata_namespace import get_public_report_metadata_namespace

# Here we are importing the route creation functions
# Each function will receive the `uploads_namespace` as a first parameter followed by other parameters if needed
from .report_register_namespace import get_report_register_namespace
from .report_snapshot_namespace import get_report_snapshot_namespace

# Here we are defining the uploads namespace which will be imported in app_builder
reports_namespace = Namespace(
    name="Reports", description="Routes available for reports", path=envs.REPORT_PATH
)
