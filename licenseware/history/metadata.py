import traceback
from datetime import datetime
from licenseware.utils.logger import log as logg
from .schemas import HistoryFilesSchema, HistorySchema
from . import utils


def get_metadata(func, func_args, func_kwargs):

    try:

        metadata = HistorySchema(
            app_id=utils.get_app_id(func, func_args, func_kwargs),
            uploader_id=utils.get_uploader_id(func, func_args, func_kwargs),
            app_name=utils.get_app_name(func, func_args, func_kwargs),
            uploader_name=utils.get_uploader_name(func, func_args, func_kwargs),
            tenant_id=utils.get_tenant_id(func, func_args, func_kwargs),
            event_id=utils.get_event_id(func, func_args, func_kwargs),
            event_type=utils.get_event_type(func, func_args, func_kwargs),
            description=utils.get_func_doc(func),
            updated_at=datetime.utcnow().isoformat(),
            files=[
                HistoryFilesSchema(
                    filename=utils.get_filename(func, func_args, func_kwargs),
                    filepath=utils.get_filepath(func, func_args, func_kwargs),
                )
            ],
            source=utils.get_func_source(func),
            func_args=utils.get_parsed_func_args(func_args),
            func_kwargs=utils.get_parsed_func_kwargs(func_kwargs),
            entities=utils.get_entities(func, func_args, func_kwargs),
        )

        return metadata

    except Exception as err:
        logg.error(err)
        if func.__name__ != "run_processing_pipeline":
            logg.error(traceback.format_exc())
        return None
