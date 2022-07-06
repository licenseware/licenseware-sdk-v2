import uuid
import string
import random
from flask import Request
from datetime import datetime
from marshmallow import Schema, INCLUDE

from licenseware import mongodata
from licenseware.mongodata import collection
from licenseware.common.constants import envs
# from licenseware.utils.flask_request import get_flask_request




def shortid(length=6):
    # Not colision prof
    # but enough when combined with tenant_id report_id
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=length))



class AllowAllSchema(Schema):
    class Meta:
        unknown = INCLUDE


class ReportSnapshot:
    def __init__(self, report: type, flask_request: Request):
        self.report = report
        self.request = flask_request    
        self.tenant_id = flask_request.headers.get("Tenantid")
        self.report_id = self.report.report_id
        self.report_uuid = str(uuid.uuid4()) 
        self.version = shortid()
        self.snapshot_date = datetime.utcnow().isoformat()


    # def get_report_data(self):
    #     # Avoid circular import 
    #     from licenseware.report_components.base_report_component import BaseReportComponent

    #     report_metadata, status_code = self.report.return_json_payload()

    #     rcomponents = []
    #     for comp in self.report.components:
    #         comp: BaseReportComponent
    #         comp_payload = comp.get_registration_payload()
    #         comp_payload["component_data"] = comp.get_data(self.request)
    #         rcomponents.append(comp_payload)

    #     report_metadata["report_components"] = rcomponents

    #     return report_metadata


    def generate_snapshot(self):
        # Avoid circular import 
        from licenseware.report_components.base_report_component import BaseReportComponent

        report_metadata, _ = self.report.return_json_payload()
        report_metadata["report_components"] = []
        report_metadata["tenant_id"] = self.tenant_id
        report_metadata["version"] = self.version
        report_metadata["report_snapshot_date"] = self.snapshot_date
        report_metadata["report_uuid"] = self.report_uuid

        mongodata.insert(
            schema=AllowAllSchema,
            data=report_metadata,
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )        

        inserted_components = set()
        for comp in self.report.components:
            comp: BaseReportComponent

            if comp.component_id in inserted_components:
                continue

            # Add component metadata
            comp_payload = comp.get_registration_payload()
            mongodata.update(
                schema=AllowAllSchema,
                match={
                    "tenant_id": self.tenant_id,
                    "report_id": self.report_id,
                    "report_uuid": self.report_uuid,
                    "version": self.version,
                    "report_snapshot_date": self.snapshot_date
                },
                new_data={
                    "report_components": [comp_payload]
                },
                collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
                append=True
            )
            
            component_data = comp.get_data(self.request)
            component_pinned = {
                "for_report_uuid": self.report_uuid,
                "component_uuid": str(uuid.uuid4()),
                "tenant_id": self.tenant_id, 
                "report_id": self.report_id,
                "component_id": comp.component_id,
                "report_snapshot_date": report_metadata["report_snapshot_date"],
                "version": report_metadata["version"]
            }

            if isinstance(component_data, list) and len(component_data) > 0:

                component_data = [ {**d, **component_pinned} for d in component_data ]
            
                with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                    col.insert_many(component_data)

            elif isinstance(component_data, dict) and len(component_data) > 0:

                component_data = {**component_data, **component_pinned} 
            
                with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                    col.insert_one(component_data)


            if comp.component_id not in inserted_components:
                inserted_components.add(comp.component_id)


           
            # if comp.component_type == "table":

                # Get data with pagination (non-breaking) and append it to report components data
                # while True:
                    
                    # flask_request = self.make_flask_request(comp, limit, skip)
                    # component_data = comp.get_data(self.request)

                    # with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                    #     col.update_one(
                    #         filter={**self.report_query, "report_components.component_id": comp.component_id},
                    #         update={
                    #             "$addToSet": {
                    #                 "report_components.$.component_data": {"$each": component_data}
                    #             }
                    #         }
                    #     )

                    # if len(component_data) == 0:
                    #     skip = 0 # reset skip
                    #     break
                    # else: # increase offset
                    #     skip += len(component_data) 

            # else:

            #     component_data = comp.get_data(self.request)

                # with collection(envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME) as col:
                #     col.update_one(
                #         filter={**self.report_query, "report_components.component_id": comp.component_id},
                #         update={
                #             "$addToSet": {
                #                 "report_components.$.component_data": {"$each": component_data}
                #             }
                #         }
                #     )


    def get_snapshot_url(self):
        self.generate_snapshot()
        return envs.BASE_URL + self.report.report_path + "/snapshot"


    def get_report_snapshot(self):

        results = mongodata.fetch(
            match={
                "tenant_id": self.tenant_id,
                "report_id": self.report.report_id
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        return results[0] if len(results) == 1 else {}

