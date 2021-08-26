'''

Documentation automatically generated with [`pdoc3`](https://pdoc3.github.io/pdoc/).

#Contents

1. [What is an `App`?](#what-is-an-app)
2. [Set environment variables](#set-environment-variables)
3. [`App` declaration](#app-declaration)
4. [`Uploader` declaration](#uploader-declaration)
5. [`Report` declaration](#report-declaration)
6. [Custom namespaces](#custom-namespaces)
7. [Endpoints from simple functions](#endpoints-from-simple-functions)
8. [The `main` file](#the-main-file)
9. [Licenseware package structure](#licenseware-package-structure)





<a name="what-is-an-app">
#What is an `App`?
</a>

Each Licenseware `App`/`Service` is responsible for:

- processing files submitted by the user;
- creating custom reports based on prcessed data from files. 


Each **APP** has:

- one or more uploaders
- one or more reports 
- one or more report components


Each **UPLOADER** has:

- one file validator class
- one file processing function


Each **REPORT** has:

- one or more report components
- report components can be attached either to app builder instance or to report builder instance







<a name="set-environment-variables">
#Set environment variables
</a>

Fist make sure you have set the environment variables:

```bash
#.env

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

Start `redis` and `mongo` databases:

```bash
make up
```








<a name="app-declaration">
# `App` declaration
</a>

`AppBuilder` class will be used to define our `App`. 
This class will handle: 

- automatic api generation;
- sending to registry service information about `uploader_builder`, `report_builder`, `report_components` and others if needed.


```py
#app_definition.py

from licenseware.app_builder import AppBuilder
from licenseware.common.constants import flags


ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)


```

The `ifmp_app` instance is now ready to attach other uploaders, reports, report components (or others) using *ifmp_app.register_X* methods.








<a name="uploader-declaration">
# `Uploader` declaration
</a>

The uploader is responsible for:

- validating files received from user;
- calculating quota for user and sending the appropiate response if quota exceded;
- uploading files to disk;
- triggering `worker_function` to process the files in the background; 

Each uploader needs a `validator_class` and a `worker_function`.  


## Creating the `worker_function`

Here is the worker function which will process the files in the background.

```py
#worker.py

from licenseware.utils.logger import log

def rv_tools_worker(event_data):
    log.info("Starting working")
    # custom logic here
    log.info("Finished working")
    
```

The `event_data` will be a dictionary with the following contents:

```js

{
    'tenant_id': "uuid4 tenant id from flask request.headers",
    'filepaths': ["absolute/path/to/files/uploaded"],
    'headers':  'flask request.headers',
    'json':  'flask request.json',
}

```

Based on given `event_data` the `worker_function` will process the files.


## Creating the `validator_class`

Here we are defining the validation and quota calculation required for each upload.

Create a new class which inherits from `UploaderValidator` and overwrite `calculate_quota` function.
Method `calculate_quota` receives a flask request as a parameter which can be used to extract files and tenant_id needed for quota calculation.

Finally, instantiate the validator class with the required parameters needed for validation.

```py
#validator.py

from typing import Tuple
from licenseware.uploader_validator import UploaderValidator


class RVToolsUploaderValidator(UploaderValidator):
    
    def calculate_quota(self, flask_request) -> Tuple[dict, int]:
    
        file_objects = flask_request.files.getlist("files[]")
        
        # custom logic for quota calculation
        
        if quota_ok:
            return {'status': 'success', 'message': 'Quota within limits'}, 200
        else:
            return {'status': 'fail', 'message': 'Quota exceeded'}, 402



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


```

If parameters provided for validating filenames and contents are not enough 
you can also overwrite `get_filenames_response` and `get_file_objects_response` methods.

- `get_filenames_response` : given a flask request object validates filenames and returns a json response, status code
- `get_file_objects_response` : given a flask request object validates filenames and contents and returns a json response, status code


Now we have `rv_tools_validator` as a `validator_class` and  `rv_tools_worker` as a `worker_function`.


```py
#uploader.py

from licenseware.uploader_builder import UploaderBuilder
from licenseware.uploader_validator import UploaderValidator

from ...worker import rv_tools_worker
from ...validator import rv_tools_validator



rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    uploader_id = 'rv_tools',
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools_validator,
    worker_function=rv_tools_worker
)


```

Great! Now we have an uploader defined!

We can later import the uploader in our main file and register it to our defined `App`.
The registering process will take care of api generation for uploaders.

```py
ifmp_app.register_uploader(rv_tools_uploader)
```

Of course defining an uploader can be defined in just one file too.













<a name="report-declaration">
# `Report` declaration
</a>

A `Report` is composed of one or more `report components`. 
Each report component will inherit from `BaseReportComponent` class.


## Creating the `Report component`

The following methods will need to be overwrited:

- `get_data` : receives a flask request needs to return data for the declared report component;
    - use `match_filters = self.get_mongo_match_filters(flask_request)` to get default pipeline filters (tenant_id and filters from front-end);

- `set_attributes` : return based on `component_type` component metadata which is used by front-end to render data received from `get_data` method;
- `set_style_attributes` : return component style metadata which is used by front-end to apply different css attributes  (width, height, color etc);

A `NotImplmentedError` exception will raise if methods mentioned up are not overwritted.


```py
#some_report_component.py

from licenseware.report_components import BaseReportComponent
from licenseware.report_components.style_attributes import style_attributes as styles
from licenseware.common.constants import icons


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
        # from licenseware.report_components.style_attributes import style_attributes as styles
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


```

Now `virtual_overview` is our `report_component`.

We can later register the component straight to the `App` or `Report`
```py
ifmp_app.register_report_component(virtual_overview)
```

## Creating the `Report`

The report can hold one or more report components. 


```py
#report.py

from licenseware.report_builder import ReportBuilder
from ...some_report_component import virtual_overview


virtualization_details_report = ReportBuilder(
    name="Virtualization Details",
    report_id="virtualization_details",
    description="This report gives you a detailed view of your virtual infrastructure.",
    connected_apps=['ifmp-service'],
    report_components=[
        virtual_overview        
    ]
)

```

We can later add the report to our main `App`

```py
ifmp_app.register_report(virtualization_details_report)
```

Reports api will be handled by the `ifmp_app` instance.






<a name="custom-namespaces">
# Custom namespaces
</a>

We are not restricted using just the apis generated from `AppBuilder` we can add new custom ones to `App`/`ifmp_app`.



```py
#some_namespace.py

from flask_restx import Namespace, Resource


ns = Namespace(
    name="Custom", 
    description="This is a custom namespace with the app prefix"
)

@ns.route("/custom-api-route")
class CustomApiRoute(Resource):    
    @ns.doc(id="custom")
    def get(self):
        return "custom-api-route"

```

We can later import the namespace created to our `main` file

```py
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')
```

`ifmp_app` will make sure it will have the app prefix.

If the custom namespace created is repetead for all apps consider adding it to `app_builder` package.







<a name="endpoints-from-simple-functions">
# Endpoints from simple functions
</a>

Class `EndpointBuilder` can be used to generate endpoints from simple functions.
The function name will be used to extract the http method and the route path (`get_custom_data_from_mongo` -->
`GET` http-method, `/get_custom_data_from_mongo` path-route)

```py
#func.py

from licenseware.endpoint_builder import EndpointBuilder

def get_custom_data_from_mongo(flask_request):
    """ Custom documentation """
    
    # Some logic here

    return "Some data"


custom_func_endpoint = EndpointBuilder(get_custom_data_from_mongo)
```

The function will receive a flask request as a parameter and will be added to `/custom_endpoint/get_custom_data_from_mongo`

Later in our `main` file: 
```py
ifmp_app.register_endpoint(custom_func_endpoint)
```









<a name="the-main-file">
#The `main` file
</a>

In the main file or in `create_app` builder function (where Flask is instantiated) we can initialize the `App` with `ifmp_app.init_app(app)` where `app` is the Flask instance. 

When `init_app` is invoked all endpoinds defined in `app_builder` will be created and registration information will be sent to registry-service if `register=True`. You can also initiate the registration to registry-service process with `ifmp_app.register_app()` 


```py

from flask import Flask
from ...app_definition import ifmp_app
from ...uploader import rv_tools_uploader
from ...some_report_component import virtual_overview
from ...report import virtualization_details_report
from ...some_namespace import ns as custom_ns
from ...func import custom_func_endpoint


app = Flask(__name__)


# These can be placed in `app_definition`  

ifmp_app.register_uploader(rv_tools_uploader)
ifmp_app.register_report_component(virtual_overview)
ifmp_app.register_report(virtualization_details_report)
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')
ifmp_app.register_endpoint(custom_func_endpoint)


# Just like any other flask extension
ifmp_app.init_app(app, register=True)    
    

if __name__ == "__main__":    
    app.run(port=4000, debug=True)


```



<a name="licenseware-package-structure">
# Licenseware package structure
</a> 

```bash

.
├── app_builder
│   ├── app_activation_route.py
│   ├── app_builder.py
│   ├── app_registration_route.py
│   ├── editable_tables_route.py
│   ├── endpoint_builder_namespace
│   │   └── __init__.py
│   ├── __init__.py
│   ├── refresh_registration_route.py
│   ├── report_components_namespace
│   │   ├── __init__.py
│   │   └── report_individual_components_namespace.py
│   ├── reports_namespace
│   │   ├── __init__.py
│   │   ├── report_components_namespace.py
│   │   ├── report_metadata_namespace.py
│   │   └── report_register_namespace.py
│   ├── tenant_registration_route.py
│   └── uploads_namespace
│       ├── filenames_validation_namespace.py
│       ├── filestream_validation_namespace.py
│       ├── __init__.py
│       ├── quota_namespace.py
│       └── status_namespace.py
├── auth
│   ├── auth.py
│   └── __init__.py
├── cli
│   └── __init__.py
├── common
│   ├── constants
│   │   ├── envs.py
│   │   ├── flags.py
│   │   ├── icons.py
│   │   ├── __init__.py
│   │   ├── quotas.py
│   │   └── states.py
│   ├── __init__.py
│   ├── serializers
│   │   ├── analysis_status_schema.py
│   │   ├── app_utilization_schema.py
│   │   ├── event_schema.py
│   │   ├── file_upload_validation_schema.py
│   │   ├── __init__.py
│   │   ├── register_app_payload_schema.py
│   │   ├── register_report_component_payload.py
│   │   ├── register_report_payload_schema.py
│   │   ├── register_uploader_payload_schema.py
│   │   └── register_uploader_status_payload_schema.py
│   └── validators
│       ├── file_validators.py
│       ├── __init__.py
│       ├── registry_payload_validators.py
│       ├── schema_validator.py
│       ├── validate_icon.py
│       └── validate_route.py
├── decorators
│   ├── auth_decorators
│   │   ├── authenticated_machine.py
│   │   ├── authorization_check.py
│   │   ├── auth_required.py
│   │   ├── __init__.py
│   │   └── machine_check.py
│   ├── failsafe_decorator.py
│   └── __init__.py
├── editable_table
│   ├── editable_table.py
│   └── __init__.py
├── endpoint_builder
│   ├── endpoint_builder.py
│   └── __init__.py
├── __init__.py
├── mongodata
│   ├── __init__.py
│   ├── mongo_connection.py
│   └── mongodata.py
├── namespace_generator
│   ├── __init__.py
│   ├── mongo_crud.py
│   ├── mongo_request.py
│   └── schema_namespace.py
├── quota
│   └── __init__.py
├── registry_service
│   ├── __init__.py
│   ├── register_all.py
│   ├── register_app.py
│   ├── register_component.py
│   ├── register_report.py
│   ├── register_uploader.py
│   └── register_upload_status.py
├── report_builder
│   ├── __init__.py
│   └── report_builder.py
├── report_components
│   ├── attributes
│   │   ├── bar_vertical.py
│   │   ├── __init__.py
│   │   ├── pie.py
│   │   ├── summary.py
│   │   └── table.py
│   ├── base_report_component.py
│   ├── build_match_expression.py
│   ├── __init__.py
│   └── style_attributes
│       ├── __init__.py
│       └── style_attributes.py
├── tenants
│   ├── active_tenants.py
│   ├── close_timeout_files.py
│   ├── __init__.py
│   └── processing_status.py
├── uploader_builder
│   ├── __init__.py
│   └── uploader_builder.py
├── uploader_validator
│   ├── file_content_validator.py
│   ├── filename_validator.py
│   ├── __init__.py
│   └── uploader_validator.py
└── utils
    ├── dramatiq_redis_broker.py
    ├── file_utils.py
    ├── __init__.py
    ├── logger.py
    └── miscellaneous.py

27 directories, 99 files

```


'''


from dotenv import load_dotenv

load_dotenv()  
