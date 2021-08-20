from flask_restx import Namespace

# Here we are importing the route creation functions 
# Each function will receive the `uploads_namespace` as a first parameter followed by other parameters if needed
from .report_register_namespace import get_report_register_namespace
from .report_metadata_namespace import get_report_metadata_namespace
from .report_components_namespace import get_report_components_namespace


# Here we are defining the uploads namespace which will be imported in app_builder
reports_namespace = Namespace(
    name="Reports",
    description="Routes available for reports",
    path="/reports"
)