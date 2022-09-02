from flask_restx import Namespace

from licenseware.common.constants import envs

from .data_sync_namespace import get_data_sync_namespace

data_sync_namespace = Namespace(
    name="DataSync",
    description="Syncronize data between apps",
    path=envs.DATA_SYNC_PATH,
)
