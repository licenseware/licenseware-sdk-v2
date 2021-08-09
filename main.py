from app.licenseware.app_builder import AppBuilder
from app.licenseware.common.constants import flags


ifmp_app = AppBuilder(
    id = 'ifmp',
    name = 'Infrastructure Mapper',
    description = 'Overview of devices and networks',
    flags = [flags.BETA]
)




