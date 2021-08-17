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

