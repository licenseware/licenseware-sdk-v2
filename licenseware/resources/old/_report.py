from licenseware.report_builder import ReportBuilder
# from app.report_components import some_report_component


# Component order is determined by it's position in the list
report_components=[
    # some_report_component       
]


{{ report_id }}_report = ReportBuilder(
    name="{{ report_id.split('_') | map('title') | join(' ') }}",
    report_id="{{ report_id }}",
    description="Add report description here",
    connected_apps=[],
    report_components=report_components
)


