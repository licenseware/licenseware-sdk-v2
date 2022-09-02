"""
Here add serializers for each dictioary/list used by the app
That way we have a consistent output, each change to serializers should be discussed

To skip validation simply comment out the validation function (see common.validators package)

"""

from .analysis_status_schema import AnalysisStatusSchema
from .event_schema import EventSchema
from .features_schema import FeaturesSchema
from .file_upload_validation_schema import FileUploadValidationSchema
from .integration_details_schema import IntegrationDetailsSchema
from .public_token_schema import PublicTokenSchema
from .quota_schema import QuotaSchema
from .register_app_payload_schema import RegisterAppPayloadSchema
from .register_report_component_payload import RegisterReportComponentPayloadSchema
from .register_report_payload_schema import RegisterReportPayloadSchema
from .register_uploader_payload_schema import RegisterUploaderPayloadSchema
from .register_uploader_status_payload_schema import RegisterUploaderStatusPayloadSchema
from .wild_schema import WildSchema
