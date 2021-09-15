# Licenseware SDK

This is the licenseware **Python3** sdk useful for quickly create apps. 
The SDK handles the repetetive actions needed for creating an app (file uploads/validation, background events, api routes and more). 
It helps you focus on processsing the files needed and creating reports.  



# Contents

1. [Quickstart](#quickstart)
2. [What is an `App`?](#what-is-an-app)
3. [Set environment variables](#set-environment-variables)
4. [`App` declaration](#app-declaration)
5. [`Uploader` declaration](#uploader-declaration)
6. [`Report` declaration](#report-declaration)
7. [Custom namespaces](#custom-namespaces)
8. [Endpoints from simple functions](#endpoints-from-simple-functions)
9. [The `main` file](#the-main-file)
10. [Licenseware CLI](#licenseware-cli) 



<a name="quickstart"></a>
# Quickstart 

Here are the steps needed for local development of an app:

- Install the sdk : `pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git`;
- Clone the repo for your service;
- CD in the cloned repo locally;
- Create a new app : `licenseware new-app odb`;
- Create a new uploader: `licenseware new-uploader lms_options`;
- Update modules `validator.py` `worker.py` as per processing requirements needs for `lms_options` uploader_id. Modules created will be found here: `app/uploaders/lms_options`
- Open the first terminal start the mock-server : `licenseware start-mock-server`;
- Open the second terminal start the redis background worker: `licenseware start-background-worker`;
- Open the third terminal start the development server: `licenseware start-dev-server`;
- Copy `docker-compose-mongo-redis.yml` file to `Documents` folder start the databases with:

```
docker-compose -f docker-compose-mongo-redis.yml up -d --remove-orphans --force-recreate
```

You will have mongoexpress running at: `http://localhost:8081/`




## Installation 

Install latest update for this package using the following pip command:
```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git

```

Install from a specific branch

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git@branch_name

```

Install from a specific tag

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git@tag_name

```

You can use `git+ssh` if you have ssh keys configured. 
Uninstall with `pip3 uninstall licenseware`.


## SDK new version release

- In `setup.py` update the package version; 
- Create a tag with that version ex: `git tag -a v0.0.11`;
- You can list available tags with `git tag -n`;
- Push created tag with `git push --tags`

Now you use pip to install it from that specific tag:

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-python3.git@v0.0.11

```

If you want to add more details regarding this package release you can `Create a new release`

- Click the link `Releases`;
- Click `Draft a new release`;
- Click `Tags`;
- Select latest tag version name;
- Add title and description for the release;

![](pics/release.gif)

Optionally you can create a wheel for this package:
```bash

python3 setup.py bdist_wheel sdist

```

And add it to binaries on the release.


## A minimal app

Bellow is a full working example of almost all features the sdk provides.

Start the services in the following order:

1. `make up` - mongo and redis;
2. `licenseware start-mock-server` - mock dependency server for our app;
3. `licenseware start-background-worker` - start the app server;
4. `licenseware start-dev-server` - start the background worker.

**Attention**

If you perviously started the docker-compose file with redis and mongo you may encounter some issues related to port already in use or docker container names. It's enough to build the image once `Documents` folder for example, after that you will always have available the mongo and redis databases.



```py
from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware.app_builder import AppBuilder
from licenseware.common.constants import (envs, filters, flags, icons,
                                              states)
from licenseware.endpoint_builder import EndpointBuilder
from licenseware.notifications import notify_upload_status
from licenseware.report_builder import ReportBuilder
from licenseware.report_components import BaseReportComponent
from licenseware.report_components.style_attributes import styles

from licenseware.uploader_builder import UploaderBuilder
from licenseware.uploader_validator import UploaderValidator
from licenseware.utils.logger import log



app = Flask(__name__)


# APP

ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)


# UPLOADERS



# Here is the worker function 
# which will process the files in the background
def rv_tools_worker(event:dict):
    
    # Event data will contain the following information
    # event = {
    #     'tenant_id': flask_request.headers.get("Tenantid"),
    #     'filepaths': valid_filepaths, 
    #     'uploader_id': self.uploader_id,
    #     'flask_request':  {**flask_body, **flask_headers},
    #     'validation_response': response
    # }

    log.info("Starting working")
    log.debug(event) # here add the processing file logic
    notify_upload_status(event, status=states.IDLE)
    log.info("Finished working")
    



# Here we are defining the validation required for each upload
# If overwriting bellow mentioned methods is not necessary you can use `UploaderValidator` directly 

class RVToolsUploaderValidator(UploaderValidator): 
    # If necessary you can overwrite bellow mentioned methods
    ...
    
    # def calculate_quota(self, flask_request) -> Tuple[dict, int]:
    # responsible for calculating quota based on tenant_id and returning a json response, status code 
    # ...
    
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
    worker_function=rv_tools_worker,
    quota_units = 1
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
        # from licenseware.report_components.style_attributes import style_attributes as styles
        style_attributes = self.build_style_attributes([
            styles.WIDTH_ONE_THIRD
            #etc
        ])
        
        return style_attributes
    
    
    def set_allowed_filters(self):
        # Provide a list of allowed filters for this component
        return [
            # You can use the build_filter method
            self.build_filter(
                column="device_name", 
                allowed_filters=[
                    filters.EQUALS, filters.CONTAINS, filters.IN_LIST
                ], 
                visible_name="Device Name", 
                # validate:bool = True # This will check field_name and allowed_filters
            ),
            # or you can create the dictionary like bellow (disadvantage no autocomplete, no checks)
            {
                "column": "database_name",
                "allowed_filters": [
                    "equals", "contains", "in_list"
                ],
                "visible_name": "Database Name"
            }
        
        ]
        


virtual_overview = VirtualOverview(
    title="Overview",
    component_id="virtual_overview",
    component_type='summary'
)

# Register component to registry-service (to act as a first class citizen)
ifmp_app.register_report_component(virtual_overview)



# Component order is determined by it's position in the list
report_components=[
    virtual_overview       
]


# Define a report wich holds one or more report components
virtualization_details_report = ReportBuilder(
    name="Virtualization Details",
    report_id="virtualization_details",
    description="This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.",
    connected_apps=['ifmp-service'],
    report_components=report_components
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


# Call init_app in the flask function factory 
ifmp_app.init_app(app)


if __name__ == "__main__":   
    
    # Register app to registry-service
    ifmp_app.register_app()
    
    app.run(port=4000, debug=True)


```


Make commands:

- `make up` and  `make down` - start and stop mongo and redis databases;
- `make mock` - start mock server which app will use for authentication, registry-service or other external services dependencies;
- `make dev` - start application with hot reload;
- `make worker` - start dramatiq worker;
- `make test` - run all unit tests.
- `make dev-docs` - this command will start a pdoc3 http server use for viewing and updating documentation for the app created;
- `make docs` - this command will generate html docs based on docstrings provided in the app;


Documentation generated can be added later to github pages.

See more about documentation creation here [`pdoc3`](https://pdoc3.github.io/pdoc/).



<a name="what-is-an-app"></a>
# What is an `App`?


Each Licenseware `App`/`Service` is responsible for:

- processing files submitted by the user;
- creating custom reports based on processed data from files. 


Each **APP** has:

- one or more uploaders
- one or more reports 
- one or more report components


Each **UPLOADER** has:

- one file validator class
- one file processing/worker function


Each **REPORT** has:

- one or more report components
- report components can be attached either to app builder instance or to report builder instance


Each **REPORT COMPONENT** has:

- one get_data method;
- one url where data can be accessed;


<a name="set-environment-variables"></a>
# Set environment variables


Fist make sure you have set the environment variables:

```

#.env

DEBUG=true
ENVIRONMENT=local
PERSONAL_SUFFIX=_222


FLASK_APP=main:app
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=4000
FLASK_DEBUG=true

APP_ID=odb
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

REDIS_HOST=redis_db_dev
REDIS_PORT=6379

```

Start `redis` and `mongo` databases:

```bash
make up
```



<a name="app-declaration"></a>
# `App` declaration


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



<a name="uploader-declaration"></a>
# `Uploader` declaration


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

from licenseware.notification import notify_upload_status
from licenseware.utils.logger import log

def rv_tools_worker(event:dict):
    log.info("Starting working")
    log.debug(event) # here add the processing file logic
    notify_upload_status(event, status=states.IDLE)
    log.info("Finished working")
    
```

The `event` will be a dictionary with the following contents:

```js

{
    'tenant_id': flask_request.headers.get("Tenantid"),
    'filepaths': valid_filepaths, 
    'uploader_id': uploader_id,
    'flask_request':  {**flask_body, **flask_headers},
    'validation_response': 'response from validator class'
}

```

Based on given `event` the `worker_function` will process the files.


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
    # Overwrite `calculate_quota`, `get_filenames_response` or `get_file_objects_response` if needed
    # Otherwise you can just instantiate the class validator from `UploaderValidator` 
    ...
    
    
    
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
you can also overwrite: `calculate_quota`, `get_filenames_response` and `get_file_objects_response` methods.

- `calculate_quota`: given a flask request object calculates quota for tenant_id based on current processing units (by default it's using len(files) got from request)
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













<a name="report-declaration"></a>
# `Report` declaration


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


    def set_allowed_filters(self):
        # Provide a list of allowed filters for this component
        return [
            # You can use the build_filter method
            self.build_filter(
                column="device_name", 
                allowed_filters=[
                    filters.EQUALS, filters.CONTAINS, filters.IN_LIST
                ], 
                visible_name="Device Name", 
                # validate:bool = True # This will check field_name and allowed_filters
            ),
            # or you can create the dictionary like bellow (disadvantage no autocomplete, no checks)
            {
                "column": "database_name",
                "allowed_filters": [
                    "equals", "contains", "in_list"
                ],
                "visible_name": "Database Name"
            }
        
        ]
        
    
        

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






<a name="custom-namespaces"></a>
# Custom namespaces


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







<a name="endpoints-from-simple-functions"></a>
# Endpoints from simple functions


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









<a name="the-main-file"></a>
# The `main` file


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




<a name="licenseware-cli"></a>
# Licenseware CLI

The licenseware sdk provides also some CLI utilities for quick development. 
You can invoke the cli with by typing licenseware in the terminal followed by --help for docs.

```

$ licenseware --help
Usage: licenseware [OPTIONS] COMMAND [ARGS]...

  Useful CLI commands for automatic code generation, files and folders
  creation.

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  build-docs               Build app html docs
  build-sdk-docs           Build licenseware sdk html docs
  new-app                  Given app_id build a new app The package...
  new-report               Given report_id build a new report The package...
  new-report-component     Given component_id build a new report component...
  new-uploader             Given uploader_id build a new uploader The...
  start-background-worker  Start the redis background worker with 4...
  start-dev-server         Start the development server (flask server with...
  start-mock-server        Start the mock server needed which is a...
  start-prod-server        Start the production server (uwsgi server with 4...

```

See help for a command by specifing the command name followed by --help

```
$ licenseware new-report-component --help

```

## Create the app from CLI 

Create the app from the terminal. 
Argument `new-app` requires an `app_id`. The id will be placed in the `.env` file.

```bash

licenseware new-app ifmp

``` 

The entire app structure will be generated 

```bash
# The cloned github repository
├── app
│   ├── common
│   │   └── __init__.py
│   ├── controllers
│   │   └── __init__.py
│   ├── __init__.py
│   ├── report_components
│   │   └── __init__.py   # create a new report component with `licenseware new-report-component component_id` 
│   ├── reports
│   │   └── __init__.py   # create a new report with `licenseware new-report report_id`
│   ├── serializers
│   │   └── __init__.py
│   ├── uploaders
│   │   └── __init__.py   # create a new uploader with `licenseware new-uploader uploader_id`
│   ├── utils
│   │    └── __init__.py
│   └── __init__.py       # here the app is instantiated and the uploaders, reports, report_components are registered to the app
├── app.log
├── docker-compose-mongo-redis.yml
├── main_example.py
├── main.py
├── makefile
├── mock_server.py
├── README.md
├── requirements.txt
├── setup.py

```

All imports will be handled by the CLI when you create a new uploader, report or report_component from the terminal.


## Create a new uploader from CLI 

Argument `new-uploader` needs a `uploader_id`

```bash

licenseware new-uploader rv_tools

``` 

```
.uploaders
├── __init__.py
└── rv_tools
    ├── __init__.py
    ├── validator.py
    └── worker.py
```

Uploader id will be `rv_tools`. Each uploader has a validator and a worker. 
All imports an routes will be handled by the licenseware sdk.
To sparse the logic you can create multiple sub-packages/modules.




## Create a new report from CLI 

Argument `new-report` needs a `report_id`

```bash

licenseware new-report virtualization_details

``` 

```
.reports
├── __init__.py
└── virtualization_details
    ├── __init__.py
    └── virtualization_details.py
```

Report id will be `virtualization_details`.
All imports an routes will be handled by the licenseware sdk.
To sparse the logic you can create multiple sub-packages/modules.




## Create a new report component from CLI 

Argument `new-report-component` needs a `component_id` and a `component_type`.

```bash

licenseware new-report-component virtual_overview summary

``` 

```
.report_components
├── __init__.py
└── virtual_overview
    ├── __init__.py
    └── virtual_overview.py
```

Component id will be `virtual_overview` and it's component type will be `summary`.
All imports an routes will be handled by the licenseware sdk.
To sparse the logic you can create multiple sub-packages/modules.




## Start develompent environments servers 

You can start from the terminal the mock server, dev/prod server and the redis background worker.

Open a terminal for each command:

```bash

licenseware start-mock-server

``` 
This will start the server that will handle mock requests to registry-service and auth-server.




```bash

licenseware start-background-worker

``` 
This will start the redis background worker server that will handle the events.


```bash

licenseware start-dev-server

``` 
This will start the flask server with auto-reload. 



# Load testing

[baton docs](https://github.com/americanexpress/baton)

```bash
baton -u http://localhost:4000 -c 10 -r 10000
```