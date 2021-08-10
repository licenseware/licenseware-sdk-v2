from flask import Flask
from flask_restx import Namespace, Resource
from app.licenseware.app_builder import AppBuilder
from app.licenseware.common.constants import flags


ifmp_app = AppBuilder(
    id = 'ifmp',
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)



app = Flask(__name__)

# Flask

@app.route('/custom-app-route')
def custom_app_route():
    return "custom-app-route"


# RestX

ns = Namespace("custom")

class CustomApiRoute(Resource):    
    @ns.doc("custom")
    def get(self):
        return "custom-api-route"
    
ns.add_resource(CustomApiRoute, "/custom-api-route")


# Build Api
api = ifmp_app.init_api(app)

# Add custom api endpoint
api.add_namespace(ns, path='/ns-prefix')






if __name__ == "__main__":
    app.run(port=4000, debug=True)