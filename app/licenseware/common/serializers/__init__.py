"""
Here add serializers for each dictioary/list used by the app
That way we have a consistent output, each change to serializers should be discussed

To skip validation simply comment out the validation function (see common.validators package)

"""

from .analysis_status_schema import AnalysisStatusSchema
from .app_utilization_schema import AppUtilizationSchema
from .event_schema import EventSchema
from .register_app_payload_schema import RegisterAppPayloadSchema
from .register_uploader_payload_schema import RegisterUploaderPayloadSchema
from .file_upload_validation_schema import FileUploadValidationSchema
from .register_uploader_status_payload_schema import RegisterUploaderStatusPayloadSchema
from .register_report_payload_schema import RegisterReportPayloadSchema
from .register_report_component_payload import RegisterReportComponentPayloadSchema