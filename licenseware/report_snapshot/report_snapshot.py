from flask import Request
from datetime import datetime
from marshmallow import Schema, fields, INCLUDE

from licenseware import mongodata
from licenseware.mongodata import collection
from licenseware.common.constants import envs
from licenseware.utils.flask_request import get_flask_request



class AllowAllSchema(Schema):
    class Meta:
        unknown = INCLUDE


class ReportSnapshot:
    def __init__(self, report: type, flask_request: Request):
        self.report = report
        self.request = flask_request    
        self.tenant_id = flask_request.headers.get("Tenantid")
        self.report_query = {
            "tenant_id": self.tenant_id,
            "report_id": self.report.report_id
        }


    def get_report_data(self):
        # Avoid circular import 
        from licenseware.report_components.base_report_component import BaseReportComponent

        report_metadata, status_code = self.report.return_json_payload()

        rcomponents = []
        for comp in self.report.components:
            comp: BaseReportComponent
            comp_payload = comp.get_registration_payload()
            comp_payload["component_data"] = comp.get_data(self.request)
            rcomponents.append(comp_payload)

        report_metadata["report_components"] = rcomponents

        return report_metadata



    def insert_report_metadata(self, report_metadata:dict):
        
        # Delete existing report snapshot
        mongodata.delete(
            match=self.report_query,
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        # Add the new report snapshot
        mongodata.insert(
            schema=AllowAllSchema,
            data=report_metadata,
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )


    def make_flask_request(self, comp, limit:int, skip:int):
        
        flask_request = None

        if comp.component_type == "table":
            flask_request = get_flask_request(
                headers={
                    "Tenantid": self.tenant_id,
                    "TenantId": self.tenant_id,
                },
                args={
                    comp.component_id + "_limit": limit,
                    comp.component_id + "_skip": skip
                }
            )

        return flask_request or self.request



    def generate_snapshot(self):
        # Avoid circular import 
        from licenseware.report_components.base_report_component import BaseReportComponent

        report_metadata, status_code = self.report.return_json_payload()
        report_metadata["report_components"] = []
        report_metadata["tenant_id"] = self.tenant_id
        report_metadata["report_snapshot_date"] = datetime.utcnow().isoformat()
        self.insert_report_metadata(report_metadata)
        
        skip = 0
        limit = 500
        inserted_components = set()
        for comp in self.report.components:
            comp: BaseReportComponent
            comp_payload = comp.get_registration_payload()

            # Base component data insert
            if comp.component_id not in inserted_components:
                comp_payload["component_data"] = []
                mongodata.update(
                    schema=AllowAllSchema,
                    match=self.report_query,
                    new_data={
                        "report_components": [comp_payload]
                    },
                    collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
                    append=True
                )
                inserted_components.add(comp.component_id)
            
            if comp.component_type == "table":
                # Get data with pagination (non-breaking) and append it to report components data
                while True:
                    
                    flask_request = self.make_flask_request(comp, limit, skip)
                    component_data = comp.get_data(flask_request)

                    with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                        col.update_one(
                            filter={**self.report_query, "report_components.component_id": comp.component_id},
                            update={
                                "$addToSet": {
                                    "report_components.$.component_data": {"$each": component_data}
                                }
                            }
                        )

                    if len(component_data) == 0:
                        skip = 0 # reset skip
                        break
                    else: # increase offset
                        skip += len(component_data) 

            else:

                component_data = comp.get_data(self.request)

                with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                    col.update_one(
                        filter={**self.report_query, "report_components.component_id": comp.component_id},
                        update={
                            "$addToSet": {
                                "report_components.$.component_data": {"$each": component_data}
                            }
                        }
                    )


    def get_snapshot_url(self):
        self.generate_snapshot()
        return envs.BASE_URL + self.report.report_path + f"/snapshot?tenant_id={self.tenant_id}"


    def get_report_snapshot(self):

        owner_tenant = self.request.args.get("tenant_id")

        if owner_tenant is None:
            raise Exception("The `tenant_id` of the report owner must be provided in the query params")

        results = mongodata.fetch(
            match={
                "tenant_id": owner_tenant,
                "report_id": self.report.report_id
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        return results[0] if len(results) == 1 else {}

