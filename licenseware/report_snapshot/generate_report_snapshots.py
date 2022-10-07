from licenseware.utils.flask_request import get_flask_request
from licenseware.utils.logger import log


def generate_report_snaphosts(tenant_id: str, created_reports):
    from licenseware.report_snapshot import ReportSnapshot

    for report in created_reports:
        log.info(f"Refreshing report: {report.report_id}...")
        # Clear current snapshot versions
        flask_request = get_flask_request(
            headers={"Tenantid": tenant_id},
        )
        rs = ReportSnapshot(report, flask_request)
        versions = rs.get_available_versions()

        if versions:
            for version in versions:
                flask_request = get_flask_request(
                    headers={"Tenantid": tenant_id},
                    json=[{"version": version}],
                )
                rs = ReportSnapshot(report, flask_request)
                rs.delete_snapshot()

        # Generate a fresh snapshot
        rs = ReportSnapshot(report, flask_request)
        versions = rs.generate_snapshot()
        log.info(f"Report Snaphost created  for report {report.report_id}{versions}")
