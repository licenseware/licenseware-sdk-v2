import uuid
import string
import random
from flask import Request
from datetime import datetime
from marshmallow import Schema, INCLUDE

from licenseware import mongodata
from licenseware.mongodata import collection
from licenseware.common.constants import envs
from licenseware.report_components.build_match_expression import build_match_expression



def shortid(length=6):
    # Not colision prof
    # but enough when combined with tenant_id report_id
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=length))



class AllowAllSchema(Schema):
    class Meta:
        unknown = INCLUDE


class ReportSnapshot:
    def __init__(self, report: type, flask_request: Request):
        from licenseware.report_builder import ReportBuilder
        self.report: ReportBuilder  = report
        self.request = flask_request    
        self.tenant_id = flask_request.headers.get("Tenantid")
        self.report_id = self.report.report_id
        self.report_uuid = str(uuid.uuid4()) 
        self.version = self.request.args.get("version", shortid()) 
        self.snapshot_date = datetime.utcnow().isoformat()

    def get_snapshot_version(self):
        snapshot = self.generate_snapshot()
        return f"Created snapshot version `{snapshot['version']}`"
         

    def get_available_versions(self):

        pipeline = [
            {
                '$match': {
                    'tenant_id': self.tenant_id, 
                    'report_id': self.report_id
                }
            }, {
                '$group': {
                    '_id': 0, 
                    'versions': {
                        '$addToSet': '$version'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'versions': '$versions'
                }
            }
        ]

        results = mongodata.aggregate(pipeline, collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME)

        return results[0] if len(results) == 1 else results


    def get_snapshot_metadata(self):

        results = mongodata.fetch(
            match={
                'tenant_id': self.tenant_id, 
                'report_id': self.report_id,
                'version': self.version,
                'report_uuid': {"$exists": True}
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        return results[0] if len(results) == 1 else results


    
    def get_mongo_match_filters(self):
        """
            Create a mongo `$match` filter with tenant_id and filters sent from frontend 
        """
        
        if self.request.json is None:
            received_filters = []
        elif isinstance(self.request.json, dict):
            received_filters = [self.request.json]
        elif isinstance(self.request.json, list):
            received_filters = self.request.json
        else:
            raise Exception("Only list or objects are accepted")

        # Inserting filter by tenant_id
        received_filters.insert(0, {
            'column': 'tenant_id', 
            'filter_type': 'equals', 
            'filter_value': self.tenant_id
        })
            
        filters = build_match_expression(received_filters)
        
        return filters


    def get_snapshot_component(self):

        limit = self.request.args.get("limit")
        skip = self.request.args.get("skip")

        if skip and not limit or limit and not skip:
            return "Limit and skip must be set together", 400

        match_filters = self.get_mongo_match_filters()
        
        pipeline = [
            {"$match": {**match_filters, **{
                'tenant_id': self.tenant_id,
                'report_id': self.report_id,
                'component_id': self.request.args.get("component_id"),
                'version': self.version,
                'for_report_uuid': {"$exists": True}
            }}},
        ]

        if skip and limit:
            pipeline.insert(-1, {"$limit": int(limit)})
            pipeline.insert(-1, {"$skip": int(skip)})


        results = mongodata.aggregate(pipeline, collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME)
      
        return results 


    def insert_report_metadata(self):

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

        return report_metadata

    def update_report_component_metadata(self, comp):
    
        comp_payload = comp.get_registration_payload()
        query_params = f"?version={self.version}&component_id={comp.component_id}"
        comp_payload["snapshot_url"] = self.report.snapshot_url + query_params

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

    def insert_component_data(self, comp, report_metadata):

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


    def generate_snapshot(self):
    
        report_metadata = self.insert_report_metadata()
              
        inserted_components = set()
        for comp in self.report.components:
        
            if comp.component_id in inserted_components:
                continue

            self.update_report_component_metadata(comp)
            self.insert_component_data(comp, report_metadata)
            
            if comp.component_id not in inserted_components:
                inserted_components.add(comp.component_id)

        return {
            "version": self.version
        }
