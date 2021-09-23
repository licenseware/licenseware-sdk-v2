from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.uploaders.rv_tools854322 import rv_tools854322_uploader
from app.report_components.virtual_overview577745 import virtual_overview577745_component
from app.reports.virtualization_details841734 import virtualization_details841734_report


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_report(virtualization_details841734_report)
App.register_report_component(virtual_overview577745_component)
App.register_uploader(rv_tools854322_uploader)

