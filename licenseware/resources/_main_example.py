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
    #     'uploader_id': 'the uploader id in our case rv_tools'
    #     'headers':  'flask request headers',
    #     'json':  'flask request json data',
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

# TODO raise component_id conflict
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
    
    