from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.report_components.virtualization_summary import virtualization_summary_component
from app.reports.virtualization_details import virtualization_details_report
from app.uploaders.rv_tools import rv_tools_uploader


App = AppBuilder(
    name = 'App Name',
    description = 'App long description',
    flags = [flags.BETA]
)


App.register_uploader(rv_tools_uploader)
App.register_report(virtualization_details_report)
App.register_report_component(virtualization_summary_component)

