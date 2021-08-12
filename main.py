from dotenv import load_dotenv
load_dotenv()  
    
    
from flask import Flask
from flask import Blueprint
from flask_restx import Namespace, Resource

from app.licenseware.app_builder import AppBuilder
from app.licenseware.uploader_builder import UploaderBuilder

from app.licenseware.utils.logger import log
from app.licenseware.common.constants import flags



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
ifmp_app.init_api(app)

# Add custom api endpoint
ifmp_app.add_namespace(custom_ns, path='/ns-prefix')


# Register app to registry-service
ifmp_app.register_app()



# UPLOADERS

def validate_rv_tools_file(file):
    return True


rv_tools_uploader = UploaderBuilder(
    name="RVTools", 
    description="XLSX export from RVTools after scanning your Vmware infrastructure.", 
    accepted_file_types=['.xls', '.xlsx'],
    validator=validate_rv_tools_file
)



ifmp_app.register_uploader(rv_tools_uploader)






if __name__ == "__main__":
    app.run(port=4000, debug=True)