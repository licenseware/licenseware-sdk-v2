from flask import Request
from datetime import datetime
from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.utils.logger import log
from marshmallow import Schema, fields, INCLUDE
from pymongo import ASCENDING
import time


class AllowAllSchema(Schema):
    class Meta:
        unknown = INCLUDE

    report_snapshot_date = fields.Str(required=True)


class ReportSnapshot:

    def __init__(self, report: type, flask_request: Request):
        self.report = report
        self.request = flask_request
        self.tenant_id = flask_request.headers.get('Tenantid')

    def add_report_components_data(self):

        report_metadata, status_code = self.report.return_json_payload()

        rcomponents = []
        for comp in self.report.components:
            comp_payload = comp.get_registration_payload()
            comp_payload['component_data'] = comp.get_data(self.request)
            rcomponents.append(comp_payload)

        report_metadata['report_components'] = rcomponents

        return report_metadata

    def generate_snapshot(self):

        report_data = self.add_report_components_data()

        report_data['tenant_id'] = self.tenant_id
        report_data['report_snapshot_date'] = datetime.utcnow().isoformat()

        mongodata.insert(
            schema=AllowAllSchema,
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
            data=report_data
        )

        return report_data

    # def get_latest_snapshot(self):
    #
    #     start = time.time()
    #
    #     # Getting latest report snapshot
    #     snapshots_collection = mongodata.get_collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME)
    #
    #     latest_snapshot = snapshots_collection.find(
    #         {
    #             'tenant_id': self.tenant_id,
    #             'report_id': self.report.report_id
    #         }
    #     ).sort("report_snapshot_date", ASCENDING).limit(1)
    #
    #     latest_snapshot = list(latest_snapshot)
    #
    #     snapshot_outdated = True
    #     if latest_snapshot:
    #         latest_snapshot = latest_snapshot[0]
    #         latest_snapshot.pop('_id')  # ObjectId is not serializable
    #
    #         counted = mongodata.document_count(
    #             match={
    #                 'tenant_id': self.tenant_id,
    #                 'updated_at': {'$gt': latest_snapshot['report_snapshot_date']}
    #             },
    #             collection=envs.MONGO_COLLECTION_ANALYSIS_NAME
    #         )
    #
    #         snapshot_outdated = True if counted > 0 else False
    #
    #     if snapshot_outdated:
    #         log.info("Returning generated report snapshot")
    #         report_data = self.generate_snapshot()
    #
    #         end = time.time()
    #         log.warning(f"Time elapsed: {end - start}")
    #         # 0.6979179382324219 ~ 0.70
    #         return report_data
    #
    #     end = time.time()
    #     log.warning(f"Time elapsed: {end - start}")
    #     # 0.02915167808532715 ~ 0.030
    #     log.info("Returning latest report snapshot")
    #     return latest_snapshot

    def get_report_data(self):

        report_data = self.generate_snapshot()

        return report_data
