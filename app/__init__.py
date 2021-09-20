from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.uploaders.rv_tools491412 import rv_tools491412_uploader
from app.report_components.virtual_overview621512 import virtual_overview621512_component
from app.reports.virtualization_details932092 import virtualization_details932092_report


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_report(virtualization_details932092_report)
App.register_report_component(virtual_overview621512_component)
App.register_uploader(rv_tools491412_uploader)

