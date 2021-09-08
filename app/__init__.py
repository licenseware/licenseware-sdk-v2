from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.uploaders.rv_tools428796 import rv_tools428796_uploader
from app.report_components.virtual_overview430156 import virtual_overview430156_component
from app.reports.virtualization_details441025 import virtualization_details441025_report


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_report(virtualization_details441025_report)
App.register_report_component(virtual_overview430156_component)
App.register_uploader(rv_tools428796_uploader)

