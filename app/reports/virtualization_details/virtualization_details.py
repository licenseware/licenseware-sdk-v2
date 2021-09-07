from licenseware.report_builder import ReportBuilder
# from app.report_components import some_report_component


# Component order is determined by it's position in the list
report_components=[
    # some_report_component       
]


virtualization_details_report = ReportBuilder(
    name="Virtualization details",
    report_id="virtualization_details",
    description="Add report description here",
    connected_apps=[],
    report_components=report_components
)

