
## QUICKSTART 

Each APP has:
- one or more uploaders
- one or more reports 

Each UPLOADER has:
- one file validator class
- one file processing function


Each REPORT has:
- one or more report components



```py
from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from flask_restx import Namespace, Resource

from app.licenseware.common.constants import flags, icons
from app.licenseware.utils.logger import log

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder
from app.licenseware.uploader_validator import UploaderValidator
from app.licenseware.report_builder import ReportBuilder
from app.licenseware.report_components import BaseReportComponent
from app.licenseware.report_components.style_attributes import style_attributes as styles

from typing import Tuple




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



# Call init_app at the end
# ifmp_app.register_app()
ifmp_app.init_app(app, register=True)




if __name__ == "__main__":
    app.run(port=4000, debug=True)



```











# REPORTS


history_report = ReportBuilder(
    id = 'history_report',
    name = 'History Report',
    description = 'History of actions made on ifmp app',
    connected_apps = ['odb'],
    flags = ['Beta'],
    # + other params
)


summary_component = ReportComponents.SummaryComponent(
    # we can generate component id from title (urls are namespaced)
    title = "Overview",  
    # will generate atributes + series
    attributes = [
        {"name": "Devices Analyzed", "icon": icons.device_icon},
        {"name": "Files Analyzed", "icon": icons.file_icon}, 
    ],
    data_method=fetch_summary_data
)

table_component = "similar to SummaryComponent"

#Single component
history_report.register_component(summary_component)
#Multiple components order defined by their positions
history_report.register_components(summary_component, table_component)
 


ifmp_app.register_report(history_report)



# CLI TOOL for generating boilerplate code

# > licenseware new uploader uploader_name (will generate boilerplate code for an uploader)
# > licenseware new report report_name (will generate boilerplate code for a report)
# > licenseware new endpoint endpoint_name (will generate boilerplate code for an endpoint)


```