from licenseware.utils.logger import log
from licenseware.report_snapshot import ReportSnapshot
from licenseware.utils.flask_request import get_flask_request


def generate_report_snaphosts(tenant_id: str, created_reports):

    for report in created_reports:
        # Clear current snapshot versions
        flask_request = get_flask_request(
            headers={"Tenantid": tenant_id},
        )
        rs = ReportSnapshot(report, flask_request)
        versions = rs.get_available_versions()
        for version in versions["versions"]:
            flask_request = get_flask_request(
                headers={"Tenantid": tenant_id},
                args={"version": version},
            )
            rs = ReportSnapshot(report, flask_request)
            rs.delete_snapshot()

        # Generate a fresh snapshot
        flask_request = get_flask_request(
            headers={"Tenantid": tenant_id},
            args={"version": version},
        )
        rs = ReportSnapshot(report, flask_request)
        version = rs.generate_snapshot()
        log.info(f"Report Snaphost created {version['version']}")
        return version
