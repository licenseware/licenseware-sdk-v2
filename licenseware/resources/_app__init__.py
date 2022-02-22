# For local develompent outside docker with `python3 main.py`
# from licenseware.utils.miscellaneous import set_environment_variables
# set_environment_variables()
from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder

App = AppBuilder(
    name='App Name',
    description='App long description',
    flags=[flags.BETA]
)



