from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.uploaders.rv_tools723908 import rv_tools723908_uploader
from app.report_components.virtual_overview173226 import virtual_overview173226_component
from app.reports.virtualization_details203484 import virtualization_details203484_report


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_report(virtualization_details203484_report)
App.register_report_component(virtual_overview173226_component)
App.register_uploader(rv_tools723908_uploader)

