import datetime
import licenseware.mongodata as m
from licenseware.serializer.analysis_status import AnalysisStatusSchema
from licenseware.utils.log_config import log
from licenseware.utils.file_timeouts import FileTimeout
from licenseware.utils.base_collection_names import (
    mongo_data_collection_name,
    mongo_utilization_collection_name,
    mongo_analysis_collection_name
)


class TenantUtils:

    def __init__(
        self,
        app_id: str = None,
        data_collection_name: str = None,
        utilization_collection_name: str = None,
        analysis_collection_name: str = None,
    ):
        if app_id:
            log.warning(
                "Parameter `app_id` is not required anymore. Will be removed in future versions")

        self.schema = AnalysisStatusSchema
        self.data_collection_name = data_collection_name or mongo_data_collection_name
        self.utilization_collection_name = utilization_collection_name or mongo_utilization_collection_name
        self.analysis_collection_name = analysis_collection_name or mongo_analysis_collection_name

    # Processing status

    def get_processing_status(self, tenant_id):
        """
            Get processing status for a tenant_id from all uploaders
        """

        FileTimeout(
            tenant_id=tenant_id,
            schema=self.analysis_collection_name
        ).close_timed_out_files()

        query = {
            'tenant_id': tenant_id, 
            '$or': [
                {
                    'files.status': 'Running'
                },
                {
                    'status': 'Running'
                }
        ]}
        results = m.document_count(
            match=query, collection=self.analysis_collection_name)
        log.info(results)

        if results > 0:
            return {'status': 'Running'}, 200
        return {'status': 'Idle'}, 200

    def get_uploader_status(self, tenant_id, uploader_id):
        """
            Get processing status for a tenant_id and the specified uploader
        """

        FileTimeout(
            tenant_id=tenant_id,
            schema=self.schema,
            analysis_collection_name=self.analysis_collection_name
        ).close_timed_out_files()

        query = {
            'tenant_id': tenant_id,
            'file_type': uploader_id,
            '$or': [
                {
                    'files.status': 'Running'
                },
                {
                    'status': 'Running'
                }
            ]
        }

        results = m.document_count(
            match=query, collection=self.analysis_collection_name)
        log.info(results)

        if results > 0:
            return {'status': 'Running'}, 200
        return {'status': 'Idle'}, 200

    # Activated tenants and tenants with data

    def clear_tenant_data(self, tenant_id):

        res = m.delete(
            match={'tenant_id': tenant_id},
            collection=self.data_collection_name
        )

        log.info(f"tenant data deleted: {res}")

    def get_activated_tenants(self, tenant_id=None):

        if not tenant_id:
            tenants_list = m.fetch(
                match='tenant_id', collection=self.utilization_collection_name
            )
            log.info(f"Activated_tenants: {tenants_list}")
            return tenants_list

        tenants_list = m.fetch(
            match={'tenant_id': tenant_id}, collection=self.utilization_collection_name
        )
        log.info(f"Activated tenant: {tenants_list}")
        return tenants_list

    def get_last_update_dates(self, tenant_id=None):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'tenant_id': '$tenant_id'
                    },
                    'last_update_date': {
                        '$max': '$updated_at'
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'tenant_id': '$_id.tenant_id',
                    'last_update_date': '$last_update_date'
                }
            }
        ]

        if tenant_id:
            pipeline.insert(0, {'$match': {'tenant_id': tenant_id}})

        last_update_dates = m.aggregate(
            pipeline, collection=self.data_collection_name)

        if not last_update_dates:
            log.info("Could not get last update dates")

        return last_update_dates

    def get_tenants_with_data(self, tenant_id=None):

        enabled_tenants = self.get_last_update_dates(tenant_id)

        if enabled_tenants:
            enabled_tenants = [{
                "tenant_id": tenant["tenant_id"],
                "last_update_date": tenant["last_update_date"]
            } for tenant in enabled_tenants]

        log.info(f"enabled_tenants: {enabled_tenants}")
        return enabled_tenants
