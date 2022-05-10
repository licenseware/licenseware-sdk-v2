'''
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
11. [Working on SDK](#working-on-sdk) 



<a name="quickstart"></a>
# Quickstart 


Basic app flow:

- User sends list of file names;
- App through the validator function of the uploader checks which files are relevant and returns a list of validated file names;
- User uploads the actual files, filtered based on the list provided by the uploader (the front-end does this);
- The uploader receives the files, runs the validation on the actual file contents (before it only had the file names), and sends the valid files to the worker_function;
- The worker function processes the files and saves them to mongo based on the structure in the serializers;
- Once the data is fully analyzed, the user can either view data as reports or as editable tables.


Here are the steps needed for local development of an app:

- Install the sdk globally or on a virtual environment (python3.8) with the following command: `pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v2.git`;
- Create a github repository following this naming convention `xxxx-service` (where `xxxx` it's an unique lowercase acronym for the service);
- Clone the repo for your service;
- CD in the cloned repo locally;
- Create a new app with the same name as the github repository: `licenseware new-app xxxx-service`;
- Run `licenseware --help` to see more commands;


Each app depends on 2 services to run:
- [Authentification service](https://github.com/licenseware/auth-service);
- [Registry service](https://github.com/licenseware/registry-service);


1. Runing the app with `stack-manager` which make available the Authentification service and Registry service:
- [Click here and follow the stack manager docs](https://github.com/licenseware/stack-manager-v2)
- If you have the stack-manager up and running and want to run the app without docker you can start locally with:
    - `make run-local` (the url will be available at `http://localhost:5000/your-app-id/docs`)


2. Running the app without `stack-manager`:

- make sure you have the default mongo connection string for mongo installed locally (`mongodb://localhost:27017/db`);
- if mongo in docker works on MAC M1 then you can use the following make commands: `make start-mongo`, `make stop-mongo`, `make logs-mongo`;
- you will have mongoexpress running at: `http://localhost:8081/`.
- `make run-nostack-mongo` (this will start the app with only mongodb as a dependency);
- open url `localhost:5000/api/docs` for swagger endpoint testing;

3. Running the app without any external dependency:
- `make run-nostack-nomongo` (this will start the app without needing mongodb up and running. 
                            It uses [mongita](https://github.com/scottrogowski/mongita) to save data. 
                            Mongita doesn't support aggregation pipelines so this method should be avoided.
                            Also you can't view data with MongoDB Compass or Mongo Express.
                        ); 


## Installation 

Clone the repo, and install the sdk with

```bash

make install-sdk

```

Or install it with pip:

```bash

pip3 install wheel_sdk/licenseware-2.0.0-py3-none-any.whl

```

Or download the sdk wheel from [this link](https://github.com/licenseware/licenseware-sdk-v2/raw/main/wheel_sdk/licenseware-2.0.0-py3-none-any.whl
) and install it with pip.



I repository is public you can install it straight from github.

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v2.git

```

Install from a specific branch

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v2.git@branch_name

```

Install from a specific tag

```bash

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v2.git@tag_name

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

pip3 install git+https://git@github.com/licenseware/licenseware-sdk-v2.git@v0.0.11

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

Start the service with `docker-compose up -d`


```py

import datetime
from trend_app_protect import wrap_wsgi_app

from flask import Flask
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware.mongodata import mongodata

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

from licenseware.schema_namespace import SchemaNamespace, MongoCrud
from licenseware.editable_table import EditableTable, metaspecs



app = Flask(__name__)


# APP

App = AppBuilder(
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
    #     'event_id': 'the current event_id of the uploaded files',
    #     'uploader_id': 'the uploader id in our case rv_tools'
    #     'flask_request':  'data as dict from flask request'
    # }
    
    log.info("Starting working")
    notify_upload_status(event_data, status=states.RUNNING)
    log.debug(event_data) # here add the processing file logic
    notify_upload_status(event_data, status=states.IDLE)
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
App.register_uploader(rv_tools_uploader)




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
App.register_report_component(virtual_overview)

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


App.register_report(virtualization_details_report)






# CUSTOM RESTX NAMESPACES
# We can add also custom namespaces to main IFMP Api

from flask import Flask, request
import flask_restx as restx
from flask_restx import Resource, Api
import marshmallow as ma
from licenseware.common import marshmallow_to_restx_model # import the converter function

app = Flask(__name__)
api = Api(app)


class SimpleNestedSchema(ma.Schema):
    simple_nested_field = ma.fields.String(required=False, metadata={'description': 'the description of simple_nested_field'})

class SimpleSchema(ma.Schema):
    simple_field1 = ma.fields.String(required=True, metadata={'description': 'the description of simple_field1'})
    simple_nest = ma.fields.Nested(SimpleNestedSchema)

# Give it as parameters the flask-restx `Api` or `Namespace` instance and the Marshmallow schema
simple_nest_from_schema = marshmallow_to_restx_model(api, SimpleSchema)


@api.route('/marshmallow-simple-nest')
class MaSimpleNest(Resource):
    # Place it where you need a restx model
    @api.expect(simple_nest_from_schema, validate=True)
    def post(self):
        return request.json
    
# Add it to main app 
# it will have the same namespace prefix /ifmp/v1/ + ns-prefix/custom-api-route
App.register_namespace(custom_ns, path='/ns-prefix')

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

App.register_endpoint(custom_func_endpoint)



# Here we are using a marshmellow schema to generate an endpoint

class DeviceData(Schema):
    
    class Meta:
        collection_name = envs.MONGO_COLLECTION_DATA_NAME
        methods = ['GET', 'PUT']
    
    tenant_id = fields.Str(required=False)
    updated_at = fields.Str(required=False)
    device_name = fields.Str(required=True)
    device_model = fields.Str(required=False)
    
    
custom_schema_endpoint = EndpointBuilder(DeviceData)

App.register_endpoint(custom_schema_endpoint)



# Namespace from marshmallow schema using SchemaNamespace class


# Defining our schema
class UserSchema(Schema):
    """ Here is some Namespace docs for user """
    name = fields.Str(required=True)
    occupation = fields.Str(required=True)


# Overwritting mongo crud methods 
class UserOperations(MongoCrud):
    
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection
        super().__init__(schema, collection)
    
    def get_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        results = mongodata.fetch(match=query, collection=self.collection)

        return {"status": states.SUCCESS, "message": results}, 200
    
    
    def post_data(self, flask_request):

        query = UserOperations.get_query(flask_request)

        data = dict(query, **{
            "updated_at": datetime.datetime.utcnow().isoformat()}
        )

        inserted_docs = mongodata.insert(
            schema=self.schema,
            collection=self.collection,
            data=data
        )

        return inserted_docs
    
    
    def put_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        updated_docs = mongodata.update(
            schema=self.schema,
            match=query,
            new_data=dict(query, **{"updated_at": datetime.datetime.utcnow().isoformat()}),
            collection=self.collection,
            append=False
        )
        
        if updated_docs == 0:
            return {"status": states.SUCCESS, "message": "Query didn't matched any data"}, 400
        
        return {"status": states.SUCCESS, "message": ""}, 200
        
    
    def delete_data(self, flask_request):

        query = self.get_query(flask_request)

        deleted_docs = mongodata.delete(match=query, collection=self.collection)

        return deleted_docs

    
    
# A restx namespace is generated on instantiation
UserNs = SchemaNamespace(
    schema=UserSchema,
    collection="CustomCollection",
    mongo_crud_class=UserOperations,
    decorators=[]
)

# Adding the namespace generated from schema to our App
user_ns = UserNs.initialize()
App.register_namespace(user_ns)



# Editable tables
# In the case we need to have on the front-end an datatable which can be modified by the user the `EditableTable` class can help us create a crud workflow from a marshmellow schema
# We can provide information about columns using the `metadata` parameter available on marshmellog `fields` object

# The metadata dict can hold the following values: 

# "editable":bool tell front-end if values from this column can be modified by the user 
# "visible": bool tell front-end if it should render column to be visible to the user
# "distinct_key":str ?
# "foreign_key":str  ?


# Using the method bellow routes will be created with SchemaNamespace class 


class DeviceTableSchema(Schema):
    
    class Meta:
        collection = envs.MONGO_COLLECTION_DATA_NAME
        methods = ['GET', 'PUT']
    
    
    _id = fields.Str(required=False, unique=True)
    tenant_id = fields.Str(required=True)
    updated_at = fields.Str(required=False)
    raw_data = fields.Str(required=False, allow_none=True)
    
    name = fields.Str(required=True, 
        metadata=metaspecs(editable=True, visible=True)
    )
    
    is_parent_to = fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata=metaspecs(
            editable=True, 
            visible=True, 
            distinct_key='name', 
            foreign_key='name'
        )  
    )

    is_child_to = fields.Str(
        required=False, allow_none=True,
        metadata=metaspecs(
            editable=True, 
            visible=True, 
            distinct_key='name', 
            foreign_key='name'
        )  
    )

    is_part_of_cluster_with =  fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata=metaspecs(
            editable=True, 
            visible=True, 
            distinct_key='name', 
            foreign_key='name'
        )  
    )
    
    is_dr_with =  fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata=metaspecs(
            editable=True, 
            visible=True, 
            distinct_key='name', 
            foreign_key='name'
        )  
    )
    
    capped = fields.Boolean(
        required=True, allow_none=False, 
        metadata=metaspecs(editable=True)
    )
    
    total_number_of_processors = fields.Integer(
        required=False, allow_none=True, 
        metadata=metaspecs(editable=True)
    )
    
    oracle_core_factor = fields.Float(
        required=False, allow_none=True, 
        metadata=metaspecs(editable=True)
    )
    
    

devices_editable_table = EditableTable(
    title="All Devices",
    schema=DeviceTableSchema
)
 

App.register_editable_table(devices_editable_table)



# Overwrite editable tables default crud methods from SchemaNamespace

# In the case the default crud methods provided by SchemaNamespace class do not fit our case we can overwrite the method needed.


# Same schema but with another name to avoid colisions
class ProcessorsTableSchema(DeviceTableSchema): ...


# custom handling of data
class InfraService:
    
    def __init__(self, schema:Schema, collection:str):
        self.schema = schema
        self.collection = collection
        
    def replace_one(self, json_data:dict):
        #custom handling of json_data
        return ["the overwritten put_data method results"]
    


# inherits from MongoCrud and overwrites `put_data` and `get_data` methods 
class ProcessorOp(MongoCrud):
    
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection
        super().__init__(schema, collection)
    
    
    def get_data(self, flask_request):
        return str(flask_request)
    
    def put_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        return InfraService(
            schema=ProcessorsTableSchema, 
            collection=envs.MONGO_COLLECTION_DATA_NAME
        ).replace_one(json_data=query)
        
    
    
# creating the restx namespace
ProcessorNs = SchemaNamespace(
    schema=ProcessorsTableSchema,
    collection=envs.MONGO_COLLECTION_DATA_NAME,
    mongo_crud_class=ProcessorOp  # feeding the custom crud class to SchemaNamespace 
).initialize()


# instantiating the editable tables
processor_table = EditableTable(
    title="All Processors",
    schema=ProcessorsTableSchema,
    namespace=ProcessorNs # here we provide our custom namespace
)
 
# same as up register the editable table
App.register_editable_table(processor_table)




# Call init_app in the flask function factory 
App.init_app(app)
# Register app to registry-service
App.register_app()

# Protect the app with TrendMicro Application Security
# app = wrap_wsgi_app(app)



if __name__ == "__main__":       
    app.run(port=4000, debug=True)
    
    
    
# Userid / Tenantid
# 3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a
# dramatiq main:App.broker -p4 --watch ./ --queues odb



```


Make commands:

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
#.envlocal

DEBUG=true
APP_HOST=http://backend.localhost
APP_ID={{ app_id }}
ENVIRONMENT=local
FILE_UPLOAD_PATH=/tmp/lware
LWARE_IDENTITY_USER=testing-service
LWARE_IDENTITY_PASSWORD=testing123
MONGO_CONNECTION_STRING=mongodb://lware:lware-secret@localhost:27017
MONGO_DATABASE_NAME=db
AUTH_SERVICE_URL=http://backend.localhost/auth
REGISTRY_SERVICE_URL=http://backend.localhost/registry-service
USE_BACKGROUND_WORKER=false

```

`USE_BACKGROUND_WORKER` set to false or not present will skip using background server and process the uploaders data straight on request.


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
    'event_id': event_id,
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
ifmp_app.register_namespace(custom_ns, path='/ns-prefix')
```

`ifmp_app` will make sure it will have the app prefix.

If the custom namespace created is repetead for all apps consider adding it to `app_builder` package.

You can also use the following CLI command to create a new boilerplate controller:
```bash
licenseware new-controller name
```

This will create the restx controller and handle the imports.



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
ifmp_app.register_namespace(custom_ns, path='/ns-prefix')
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
  build-docs            Build app html docs
  build-sdk-docs        Build licenseware sdk html docs
  create-tests          Create tests from swagger docs Command example: >>...
  new-app               Given app_id build a new app The package structure...
  new-report            Given report_id build a new report The package...
  new-report-component  Given component_id and component_type build a new...
  new-uploader          Given uploader_id build a new uploader The package...
  recreate-files        Recreate files that are needed but missing

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
.
├── app
│   ├── common
│   │   └── __init__.py
│   ├── controllers
│   │   └── __init__.py
│   ├── __init__.py
│   ├── report_components
│   │   └── __init__.py
│   ├── reports
│   │   └── __init__.py
│   ├── serializers
│   │   └── __init__.py
│   ├── services
│   │   └── __init__.py
│   ├── uploaders
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── app.log
├── CHANGELOG.md
├── cloudformation-templates
│   ├── odb-api_prod.yml
│   └── odb-api.yml
├── deploy
│   └── jupyter
│       ├── docker-compose.yml
│       └── requirements.txt
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── Dockerfile.stack
├── main.py
├── makefile
├── Procfile
├── Procfile.stack
├── README.md
├── requirements-dev.txt
├── requirements-tests.txt
├── requirements.txt
├── setup.py
├── test_files
├── tests
│   ├── __init__.py
│   └── test_starter.py
├── tox.ini
└── version.txt

14 directories, 32 files
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


**For more information inspect licenseware package**


<a name="working-on-sdk"></a>
# Working on SDK

- Each new feature should be placed in a package
- Add only features that apply to all or most apps
- # TODO




# Load testing

[baton docs](https://github.com/americanexpress/baton)

```bash
baton -u http://localhost/appid/yourendpoint -c 10 -r 10000
```

'''
