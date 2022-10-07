import random
import string
import uuid
from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from flask import Request
from marshmallow import INCLUDE, Schema

from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.mongodata import collection
from licenseware.report_components.build_match_expression import build_match_expression
from licenseware.utils.flask_request import get_flask_request
from licenseware.utils.logger import log


def insert_mongo_limit_skip_filters(skip: int, limit: int, pipeline: List[dict]):

    if isinstance(skip, str):
        try:
            skip = int(skip)
        except:
            skip = None

    if isinstance(limit, str):
        try:
            limit = int(limit)
        except:
            limit = None

    if not isinstance(skip, int):
        return pipeline

    if not isinstance(limit, int):
        return pipeline

    if skip < 0:  # pragma no cover
        return pipeline

    if limit <= 0:
        return pipeline

    pipeline = pipeline + [{"$skip": skip}]
    pipeline = pipeline + [{"$limit": limit}]

    return pipeline


def shortid(length=6):
    # Not colision prof
    # but enough when combined with tenant_id
    return "".join(random.choices(string.digits + string.ascii_uppercase, k=length))


class AllowAllSchema(Schema):
    class Meta:
        unknown = INCLUDE


class ReportSnapshot:
    def __init__(self, report: type, flask_request: Request):
        from licenseware.report_builder import ReportBuilder

        self.report: ReportBuilder = report
        self.request = flask_request
        self.tenant_id = flask_request.headers.get("Tenantid")
        self.report_id = self.report.report_id
        self.report_uuid = str(uuid.uuid4())
        self.version = self.request.args.get("version") or shortid()
        self.snapshot_date = datetime.utcnow().isoformat()

    def get_snapshot_version(self):
        snapshot = self.generate_snapshot()
        return f"Created snapshot version `{snapshot['version']}`"

    def get_available_versions(self):

        pipeline = [
            {"$match": {"tenant_id": self.tenant_id, "report_id": self.report_id}},
            {"$group": {"_id": 0, "versions": {"$addToSet": "$version"}}},
            {"$project": {"_id": 0, "versions": "$versions"}},
        ]

        results = mongodata.aggregate(
            pipeline, collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        # [{'versions': ['DS4PZM']}]
        return results[0]["versions"] if results else []

    def get_snapshot_metadata(self):

        results = mongodata.fetch(
            match={
                "tenant_id": self.tenant_id,
                "report_id": self.report_id,
                "version": self.version,
                "report_uuid": {"$exists": True},
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        return results[0] if len(results) == 1 else results

    def get_mongo_match_filters(self, getlist=True):
        """
        Create a mongo `$match` filter with tenant_id and filters sent from frontend
        """

        received_filters = []
        if isinstance(self.request.json, dict):
            received_filters = [self.request.json]

        parsed_filters = []
        for filter in received_filters:
            if isinstance(filter, dict) and sorted(
                ["column", "filter_type", "filter_value"]
            ) == sorted(filter.keys()):
                parsed_filters.append(filter)

        # Inserting filter by tenant_id
        parsed_filters.insert(
            0,
            {
                "column": "tenant_id",
                "filter_type": "equals",
                "filter_value": self.tenant_id,
            },
        )

        filters = build_match_expression(parsed_filters)

        return [filters] if getlist else filters

    def get_snapshot_component(self):

        limit = self.request.args.get("limit")
        skip = self.request.args.get("skip")

        match_filters = self.get_mongo_match_filters(False)

        pipeline = [
            {
                "$match": {
                    **match_filters,
                    **{
                        "tenant_id": self.tenant_id,
                        "report_id": self.report_id,
                        "component_id": self.request.args.get("component_id"),
                        "version": self.version,
                        "for_report_uuid": {"$exists": True},
                    },
                }
            },
        ]

        pipeline = insert_mongo_limit_skip_filters(skip, limit, pipeline)

        log.warning(f"Helooo: {pipeline}")

        results = mongodata.aggregate(
            pipeline, collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME
        )

        return results

    def update_snapshot(self):

        new_data = self.request.json["new_data"]
        new_data.pop("_id", None)

        updated_doc = mongodata.update(
            schema=AllowAllSchema,
            match={
                "_id": self.request.json["_id"],
                "tenant_id": self.tenant_id,
            },
            new_data=new_data,
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        if updated_doc:
            return new_data
        return "Didn't found any match on field `_id` on this `tenant_id`", 400

    def _id_belongs_to_report(self, _id: str):

        results = mongodata.document_count(
            match={
                "_id": _id,
                "tenant_id": self.tenant_id,
                "report_uuid": {"$exists": True},
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        return bool(results)

    def _delete_by_ids(self):

        ids_to_delete = []
        for d in self.request.json:
            if not d.get("_id"):
                continue
            # we can't delete report metadata and leave it's components hanging
            if self._id_belongs_to_report(d["_id"]):
                continue
            ids_to_delete.append(ObjectId(d["_id"]))

        deleted_docs = mongodata.delete(
            match={
                "_id": {"$in": ids_to_delete},
                "tenant_id": self.tenant_id,
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        return deleted_docs

    def _delete_by_versions(self):

        versions_to_delete = []
        for d in self.request.json:
            if not d.get("version"):
                continue
            versions_to_delete.append(d["version"])

        deleted_docs = mongodata.delete(
            match={
                "version": {"$in": versions_to_delete},
                "tenant_id": self.tenant_id,
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        return deleted_docs

    def _delete_by_component_uuids(self):

        component_uuids_to_delete = []
        for d in self.request.json:
            if not d.get("component_uuid"):
                continue
            component_uuids_to_delete.append(d["component_uuid"])

        deleted_docs = mongodata.delete(
            match={
                "component_uuid": {"$in": component_uuids_to_delete},
                "tenant_id": self.tenant_id,
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        return deleted_docs

    def _delete_by_report_uuids(self):

        report_uuids_to_delete = []
        for d in self.request.json:
            if not d.get("report_uuid"):
                continue
            report_uuids_to_delete.append(d["report_uuid"])

        d1 = mongodata.delete(
            match={
                "report_uuid": {"$in": report_uuids_to_delete},
                "tenant_id": self.tenant_id,
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        d2 = mongodata.delete(
            match={
                "for_report_uuid": {"$in": report_uuids_to_delete},
                "tenant_id": self.tenant_id,
            },
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
        )

        deleted_docs = d1 + d2

        return deleted_docs

    def delete_snapshot(self):

        self._delete_by_ids()
        self._delete_by_versions()
        self._delete_by_component_uuids()
        self._delete_by_report_uuids()

        return "Requested items were deleted"

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
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
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
                "report_snapshot_date": self.snapshot_date,
            },
            new_data={"report_components": [comp_payload]},
            collection=envs.MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME,
            append=True,
        )

    def insert_component_data(self, comp, report_metadata):

        flask_request = get_flask_request(
            headers={
                "Tenantid": self.request.headers.get("Tenantid"),
                "TenantId": self.request.headers.get("Tenantid"),
                "Authorization": self.request.headers.get("Authorization"),
            },
            json=self.get_mongo_match_filters(),
        )

        component_data = comp.get_data(flask_request)
        component_pinned = {
            "for_report_uuid": self.report_uuid,
            "component_uuid": str(uuid.uuid4()),
            "tenant_id": self.tenant_id,
            "report_id": self.report_id,
            "component_id": comp.component_id,
            "report_snapshot_date": report_metadata["report_snapshot_date"],
            "version": report_metadata["version"],
        }

        if isinstance(component_data, list) and len(component_data) > 0:
            component_data = [{**d, **component_pinned} for d in component_data]
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

        return {"version": self.version}
