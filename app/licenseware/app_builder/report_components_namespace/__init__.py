from flask_restx import Namespace
from app.licenseware.common.constants import envs


# Here we are importing the route creation functions 
# Each function will receive the `uploads_namespace` as a first parameter followed by other parameters if needed
from .report_individual_components_namespace import get_report_individual_components_namespace


# Here we are defining the uploads namespace which will be imported in app_builder
report_components_namespace = Namespace(
    name="Report Components",
    description="Routes available for report components",
    path=envs.REPORT_COMPONENT_PATH
)