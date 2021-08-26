
## QUICKSTART 

Each APP has:
- one or more uploaders
- one or more reports 

Each UPLOADER has:
- one file validator class
- one file processing function


Each REPORT has:
- one or more report components
- report components can be attached either to app builder instance or to report builder instance




```py
from dataclasses import field
import re
from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from app.licenseware.common.constants import flags, icons, envs
from app.licenseware.utils.logger import log

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder
from app.licenseware.uploader_validator import UploaderValidator
from app.licenseware.report_builder import ReportBuilder
from app.licenseware.report_components import BaseReportComponent
from app.licenseware.report_components.style_attributes import style_attributes as styles
from app.licenseware.endpoint_builder import EndpointBuilder

from typing import Tuple




app = Flask(__name__)

# This hides flask_restx `X-fields` from swagger headers  
app.config['RESTX_MASK_SWAGGER'] = False



# APP

ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)


# UPLOADERS


# Here is the worker function 
# which will process the files in the background
def rv_tools_worker(event_data):
    
    # Event data will contain the following information
    # event_data = {
    #     'tenant_id': 'the tenant_id from request',
    #     'filepaths': 'absolute file paths to the files uploaded',
    #     'headers':  'flask request headers',
    #     'json':  'flask request json data',
    # }
    
    log.info("Starting working")
    log.debug(event_data)
    log.info("Finished working")
    



# Here we are defining the validation required for each upload

class RVToolsUploaderValidator(UploaderValidator):
    
    def calculate_quota(self, flask_request) -> Tuple[dict, int]:
        
        file_objects = flask_request.files.getlist("files[]")
        # each set of files have a different way of calculating quota
        # TODO
        # - calculate quota based on user_id (send a get request with tenant_id query param to auth-service /user_id_from_tenant_id)
        # - gather all docs from IFMPUtilization collection with user_id
        # - calculate quota based on user plan (if plan free calculate quota. if plan paid do something else, probably send a default quota within limits?)
        
        
        # After calculation return one of bellow responses:
        # return {'status': 'fail', 'message': 'Quota exceeded'}, 402
        return {'status': 'success', 'message': 'Quota within limits'}, 200
    
    # If necessary you can overwrite the way validation of filenames and file binary it's done
    
    # def get_filenames_response(self, flask_request): 
    # responsible for validating filenames and returning a json response, status code
    # ...
    
    # def get_file_objects_response(self, flask_request): 
    #   responsible for validating filenames, their contents and returning a json response, status code
    # ...
    
    

rv_tools_validator = RVToolsUploaderValidator(
    filename_contains = ['RV', 'Tools'],
    filename_endswith = ['.xls', '.xlsx'],
    ignore_filenames  = ['skip_this_file.csv'],
    required_input_type = "excel",
    min_rows_number = 1,
    required_sheets = ['tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'],
    required_columns = [
        'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
        'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
        'Name', 'NumCpuThreads', 'NumCpuCores'
    ]
)

# Here we are creating the uploader 
# Notice we are providing the the validator created up to `validator_class` parameter
# `worker_function` will be called when `uploader_id` is triggered
# The `uploader_id` event is triggered when files are uploaded to `/uploads/uploader_id/files` route

rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    uploader_id = 'rv_tools',
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools_validator,
    worker_function=rv_tools_worker
)

# Here we are:
# - adding the uploader to the main app (uploaders list)
# - sending uploader information to registry-service
ifmp_app.register_uploader(rv_tools_uploader)




# REPORTS


class VirtualOverview(BaseReportComponent):
            
    def __init__(
        self, 
        title: str, 
        component_id: str, 
        component_type: str
    ):
        self.title = title
        self.component_id = component_id
        self.component_type = component_type
        
        super().__init__(**vars(self))
        
        
    def get_data(self, flask_request):
        
        match_filters = self.get_mongo_match_filters(flask_request)
        
        log.info(match_filters)

        return ['mongo pipeline result']
    
    
    def set_attributes(self):
        
        # Short hand based on value_key
        # See based on component type funcs from: licenseware.report_components.attributes
        value_key_and_icon = [
            ("number_of_devices", icons.SERVERS), 
            ("number_of_databases", icons.DATABASE_ROUNDED)
        ]

        # Set values straight to self.attributes
        self.attributes = self.build_attributes(value_key_and_icon)
        
        
        # Or raw dict (same results are achived using the method up)
        
        attributes = {'series': [
            {
                'value_description': 'Number of devices',
                'value_key': 'number_of_devices',
                'icon': 'ServersIcon'
            },
            {
                'value_description': 'Number of databases',
                'value_key': 'number_of_databases',
                'icon': 'DatabaseIconRounded'
            }
        ]}
        
        # You can also return attributes
        return attributes
        
        
    def set_style_attributes(self):
        
        # You can set a dictionary directly or return a dict like bellow
        self.style_attributes = {
            'width': '1/3'
        }
        
        # or import `style_attributes` dataclass
        # from app.licenseware.report_components.style_attributes import style_attributes as styles
        style_attributes = self.build_style_attributes([
            styles.WIDTH_ONE_THIRD
            #etc
        ])
        
        return style_attributes
        

virtual_overview = VirtualOverview(
    title="Overview",
    component_id="virtual_overview",
    component_type='summary'
)


# Register component to registry-service (to act as a first class citizen)
ifmp_app.register_report_component(virtual_overview)


# Define a report wich holds one or more report components
virtualization_details_report = ReportBuilder(
    name="Virtualization Details",
    report_id="virtualization_details",
    description="This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.",
    connected_apps=['ifmp-service'],
    report_components=[
        virtual_overview        
    ]
)


ifmp_app.register_report(virtualization_details_report)






# CUSTOM RESTX NAMESPACES
# We can add also custom namespaces to main IFMP Api

custom_ns = Namespace(
    name="Custom", 
    description="This is a custom namespace with the app prefix"
)

@custom_ns.route("/custom-api-route")
class CustomApiRoute(Resource):    
    @custom_ns.doc("custom")
    def get(self):
        return "custom-api-route"
    
# Add it to main app 
# it will have the same namespace prefix /ifmp/v1/ + ns-prefix/custom-api-route
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')

# If the namespace defined up it's used on all apps 
# add it to licenseware sdk in app_builder default routes



# EndpointBuilder

# Endpoints can be generated from functions or marshmellow schemas
# add http method as a prefix to schema or function handler (get_some_data, PostDeviceDataSchema etc)

# Here we are using a function to create an endpoint like /custom_endpoint/custom_data_from_mongo

def get_custom_data_from_mongo(flask_request):
    """ Custom documentation """
    
    # Some logic here

    return "Some data"


custom_func_endpoint = EndpointBuilder(get_custom_data_from_mongo)

ifmp_app.register_endpoint(custom_func_endpoint)

# Here we are using a schema to generate an endpoint

class GetDeviceData(Schema):
    
    class Meta:
        collection_name = envs.MONGO_COLLECTION_DATA_NAME
    
    tenant_id = fields.Str(required=False)
    updated_at = fields.Str(required=False)
    name = fields.Str(required=True)
    occupation = fields.Str(required=False)
    
    
custom_schema_endpoint = EndpointBuilder(GetDeviceData)


ifmp_app.register_endpoint(custom_schema_endpoint)




if __name__ == "__main__":
    
    # Call init_app at the end
    # ifmp_app.register_app()
    ifmp_app.init_app(app, register=True)
    
    
    app.run(port=4000, debug=True)


```

Required environment variables

```bash

FLASK_APP=main:app

APP_ID=ifmp
APP_HOST=http://localhost:5000

LWARE_IDENTITY_USER=John
LWARE_IDENTITY_PASSWORD=secret

AUTH_SERVICE_URL=http://localhost:5000/auth
AUTH_SERVICE_USERS_URL_PATH=/users
AUTH_SERVICE_MACHINES_URL_PATH=/machines

REGISTRY_SERVICE_URL=http://localhost:5000/registry-service

FILE_UPLOAD_PATH=/tmp/lware

MONGO_ROOT_USERNAME=John
MONGO_ROOT_PASSWORD=secret
MONGO_HOSTNAME=localhost
MONGO_PORT=27017
MONGO_DATABASE_NAME=db
MONGO_CONNECTION_STRING=mongodb://${MONGO_HOSTNAME}:${MONGO_PORT}/${MONGO_DATABASE_NAME}


REDIS_HOST=redis_db_sdk
REDIS_PORT=6379

```



Make commands:

- `make up` and  `make down` - start and stop mongo and redis databases;
- `make mock` - start mock server which app will use for authentication, registry-service or other external services dependencies;
- `make dev` - start application with hot reload;
- `make worker` - start dramatiq worker;
- `make test` - run all unit tests.
- `make dev-docs` - start [`pdoc3`](https://pdoc3.github.io/pdoc/) documentation server, which auto generates documentation from markdown doc strings to html.
- `make docs` - generate `docs` folder with all documantation generated in html format (can be added later to github pages `github.io/python3-licenseware-sdk-docs`)




