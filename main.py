from dotenv import load_dotenv
load_dotenv()  

from typing import Tuple

from flask import Flask
from app.licenseware.common.constants import flags
from app.licenseware.utils.logger import log

from flask_restx import Namespace, Resource

from app.licenseware.app_builder import AppBuilder

from app.licenseware.uploader_builder import UploaderBuilder
from app.licenseware.uploader_validator import UploaderValidator

from app.licenseware.report_builder import ReportBuilder
from app.licenseware.report_components import (
    SummaryReportComponent,
    DetailedSummaryReportComponent,
    PieChartReportComponent,
    BarVerticalChartReportComponent,
    TableReportComponent,
    style_props,
    data_props
)

from app.licenseware.common.constants import icons




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


def get_virtual_overview_component_data(tenant_id, filters=None):
    pipeline = ["mongo db aggregation pipeline"]
    data = pipeline
    return data
    
# TODO make component independent from report (has it's own url)
# inherit from BaseReportComponent
# register component to register service
# 

summary_virtual_overview = SummaryReportComponent(
    title="Overview",
    component_id="virtual_overview",
    fetch_function=get_virtual_overview_component_data,
    machine_names_icons = [
        ("number_of_devices", "ServersIcon"), 
        ("number_of_databases", "DatabaseIconRounded")
    ],
    style_props=[
        style_props.WIDTH_ONE_THIRD
    ],
    main_icon=icons.SERVERS
)


virtualization_details_report = ReportBuilder(
    name="Virtualization Details",
    report_id="virtualization_details",
    description="This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.",
    connected_apps=['ifmp-service'],
    report_components=[
        summary_virtual_overview        
    ]
)


ifmp_app.register_report(virtualization_details_report)


# SummaryReportComponent,
# DetailedSummaryReportComponent,
# PieChartReportComponent,
# BarVerticalChartReportComponent,
# TableReportComponent









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
