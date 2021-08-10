from flask import Flask
# from flask import Blueprint
from app.licenseware.app_builder import AppBuilder
from app.licenseware.common.constants import flags


app = Flask(__name__)
# bp = Blueprint('api', __name__)



ifmp_app = AppBuilder(
    id = 'ifmp',
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)


ifmp_app.init_app(app)
# ifmp_app.init_app(bp)



# app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(port=4000, debug=True)