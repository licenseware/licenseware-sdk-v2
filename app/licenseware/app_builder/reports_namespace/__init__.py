from flask_restx import Namespace

# Here we are importing the route creation functions 
# Each function will receive the `uploads_namespace` as a first parameter followed by other parameters if needed
# from .filenames_validation_namespace import get_filenames_validation_namespace


# Here we are defining the uploads namespace which will be imported in app_builder
reports_namespace = Namespace(
    name="Reports",
    description="Routes available for reports",
    path="/reports"
)