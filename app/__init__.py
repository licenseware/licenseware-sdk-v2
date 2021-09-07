from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.uploaders.rv_tools import rv_tools_uploader
from app.report_components.virtual_overview import virtual_overview_component
from app.reports.virtualization_details import virtualization_details_report


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_report(virtualization_details_report)
App.register_report_component(virtual_overview_component)
App.register_uploader(rv_tools_uploader)

