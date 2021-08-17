
## QUICKSTART 

Each APP has:
- one or more uploaders
- one or more reports 

Each UPLOADER has:
- one file validator class

Each REPORT has:
- one or more report components



```py

from dotenv import load_dotenv
load_dotenv()  

from typing import Tuple

from flask import Flask
from app.licenseware.common.constants import flags
from app.licenseware.utils.logger import log

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder
from app.licenseware.uploader_validator import UploaderValidator


app = Flask(__name__)

# APP

ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)



# UPLOADERS


# Here we are defining the validation required for each upload

class RVToolsUploaderValidator(UploaderValidator):
    
    def calculate_quota(self, flask_request) -> Tuple[dict, int]:
        
        file_objects = flask_request.files.getlist("files[]")
        # each set of files have a different way of calculating quota
        
        return {'status': 'success', 'message': 'Quota within limits'}, 200
    
    # If necessary you can overwrite the way 
    # validation of filenames and file binary it's done
    # Bellow functions are available for overwrite

    # def get_filenames_response(self, flask_request): 
    # responsible for validating filenames and returning a json reponse, status code
    # ...
    
    # def get_file_objects_response(self, flask_request): 
    #   responsible for validating filenames, their contents and returning a json reponse, status code
    # ...
    
    

rv_tools_validator = RVToolsUploaderValidator(
    uploader_id = 'rv_tools',
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

rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools_validator
)

# Here we are:
# - adding the uploader to the main app (uploaders list)
# - sending uploader information to registry-service
ifmp_app.register_uploader(rv_tools_uploader)


# TODO REPORTS


# Invoke the init_app after registering uploaders/reports/namespaces 
# ifmp_app.register_app()
ifmp_app.init_app(app, register=True)




if __name__ == "__main__":
    app.run(port=4000, debug=True)


```


# Basic flask_dramatiq setup 

```py

from flask_dramatiq import Dramatiq

broker = Dramatiq(broker_cls='dramatiq.brokers.redis:RedisBroker')

@broker.actor(max_retries=3, actor_name='rv_tools', queue_name='ifmp')
def rv_tools_worker(data):
    log.warning("helloo from dramatiq")


@app.route("/dramatiq")
def myhandler():
    rv_tools_worker.send()
    # broker.actors[actor_name].send(event)
    return "task sent to dramatiq"


event = {
    "tenant_id": request_obj.headers.get("TenantId"),
    "files": ",".join(saved_files)
}


# .
# .
# .

app = Flask(__name__)

broker.init_app(app) 


# Needs FLASK_APP env set to attach dramatiq worker cli
# FLASK_APP=main:app
# flask worker -p4


```




# OLD



# Conventions over configuration


## APP description

Each APP is reponsible for:
- processing one or more files aka `uploaders`;
- returning based on available proccesed data one or more `reports`;





"""

from flask import Flask
from flask import Blueprint
from flask_restx import Namespace, Resource

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder

from app.licenseware.auth import Authenticator

from app.licenseware.utils.logger import log
from app.licenseware.common.constants import flags



Authenticator.connect()


ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)



app = Flask(__name__)

# Flask

# Basic
@app.route('/custom-app-route')
def custom_app_route():
    return "custom-app-route"


# Blueprints
bp = Blueprint("custom_bp", __name__)

@bp.route('/custom-bp-route')
def custom_bp_route():
    return "custom-bp-route"

app.register_blueprint(bp)


# RestX

custom_ns = Namespace("custom")

class CustomApiRoute(Resource):    
    @custom_ns.doc("custom")
    def get(self):
        return "custom-api-route"
    
custom_ns.add_resource(CustomApiRoute, "/custom-api-route")


# Build Api
ifmp_app.init_app(app)

# Add custom api endpoint
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')


# UPLOADERS

def validate_rv_tools_file(file):
    return True


class ValidateRVTOOLS:
    
    quota = 1
    #quota based on plan type
    #free plan quota limited
    #paid unlimited/per-use
    #check AnalysisStats
    


rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator=validate_rv_tools_file
)



ifmp_app.register_uploader(rv_tools_uploader)


# Register app to registry-service
ifmp_app.register_app()


if __name__ == "__main__":
    app.run(port=4000, debug=True)


"""


```


## Basic app structure

```bash
APP
├── common
├── endpoints
├── reports
├── uploaders
└── utils
```

- `common`,`utils` : common functionality;
- `endpoints` : custom specific routes out of scope for `reports` and `uploaders`;
- `reports`   : data aggregators for a specific report;
- `uploaders` : processing file handlers responsible for getting data into database;


## Extended app structure

```bash
APP
├── common
│   └── __init__.py
├── endpoints
│   ├── custom_endpoint_name
│   │   ├── controllers
│   │   ├── serializers
│   │   └── services
│   └── __init__.py
├── __init__.py
├── reports
│   ├── __init__.py
│   ├── report_consolidated
│   │   └── __init__.py
│   └── report_name_x
│       └── __init__.py
├── uploaders
│   ├── __init__.py
│   ├── power_cli
│   │   ├── controllers
│   │   ├── __init__.py
│   │   ├── serializers
│   │   ├── services
│   │   └── workers
│   └── rv_tools
│       ├── controllers
│       ├── __init__.py
│       ├── serializers
│       ├── services
│       └── workers
└── utils
    └── __init__.py
```



https://umongo.readthedocs.io/en/latest/
https://umongo.readthedocs.io/en/latest/userguide.html



```python
from dotenv import load_dotenv
load_dotenv()  
    
    
from flask import Flask
from app.licenseware.common.constants import flags
from app.licenseware.utils.logger import log

from app.licenseware.app_builder import AppBuilder

from app.licenseware.uploader_builder import UploaderBuilder
from app.licenseware.uploader_validator import UploaderValidator


app = Flask(__name__)


ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)


# UPLOADERS

# You can inherit from UploadValidator and overwrite defaults 
class OverwriteUploaderValidator(UploaderValidator):
    pass


# This is the default way you can create a file validator
rv_tools_validator = UploaderValidator(
    uploader_id = 'rv_tools',
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


rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools_validator
)


ifmp_app.register_uploader(rv_tools_uploader)


# Invoke the init_app after registering uploaders/reports/namespaces 
ifmp_app.register_app()
ifmp_app.init_app(app, register=True)




if __name__ == "__main__":
    app.run(port=4000, debug=True)
















"""

from flask import Flask
from flask import Blueprint
from flask_restx import Namespace, Resource

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder

from app.licenseware.auth import Authenticator

from app.licenseware.utils.logger import log
from app.licenseware.common.constants import flags



Authenticator.connect()


ifmp_app = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)



app = Flask(__name__)

# Flask

# Basic
@app.route('/custom-app-route')
def custom_app_route():
    return "custom-app-route"


# Blueprints
bp = Blueprint("custom_bp", __name__)

@bp.route('/custom-bp-route')
def custom_bp_route():
    return "custom-bp-route"

app.register_blueprint(bp)


# RestX

custom_ns = Namespace("custom")

class CustomApiRoute(Resource):    
    @custom_ns.doc("custom")
    def get(self):
        return "custom-api-route"
    
custom_ns.add_resource(CustomApiRoute, "/custom-api-route")


# Build Api
ifmp_app.init_app(app)

# Add custom api endpoint
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')


# UPLOADERS

def validate_rv_tools_file(file):
    return True


class ValidateRVTOOLS:
    
    quota = 1
    #quota based on plan type
    #free plan quota limited
    #paid unlimited/per-use
    #check AnalysisStats
    


rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator=validate_rv_tools_file
)



ifmp_app.register_uploader(rv_tools_uploader)


# Register app to registry-service
ifmp_app.register_app()


if __name__ == "__main__":
    app.run(port=4000, debug=True)


"""



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


# Attrs for ifmp_app

ifmp_app.restx_api
ifmp_app.flask_app



# CLI TOOL for generating boilerplate code

# > licenseware new uploader uploader_name (will generate boilerplate code for an uploader)
# > licenseware new report report_name (will generate boilerplate code for a report)
# > licenseware new endpoint endpoint_name (will generate boilerplate code for an endpoint)


```