from typing import Callable, Dict, List

from flask import Request

from licenseware import history
from licenseware.common.constants import envs, states
from licenseware.common.validators.validate_event import validate_event
from licenseware.notifications import notify_upload_status
from licenseware.quota import Quota
from licenseware.registry_service.register_uploader import register_uploader
from licenseware.uploader_encryptor import UploaderEncryptor
from licenseware.uploader_validator.uploader_validator import UploaderValidator
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import get_flask_request_dict


class UploaderBuilder:
    """

    name:str - name of the uploader
    uploader_id:str - uploader_id, this should be unique for each app declared
    description:str - description of this uploader, what type of files it accepts
    accepted_file_types:list - accepted file formats .xlsx, .pdf etc
    validator_class: UploaderValidator -  this is a UploaderValidator class instance
    worker_function: Callable - this is responsible for processing the received files (receives a dict with tenant_id and absolute paths to files). If None upload will e skipped.
    quota_units:int - number of units allowed to be processed for free each month. If None upload will e skipped.
    flags:list = [] - stage of the development see constants.flags dataclass to see/add values


    You can add extra query parameters on uploaders either on filename validation or file upload

    query_params_on_validation = {
        'param1_name': 'param description',
        'param2_name': 'param description',
        'param3_name': 'param description',
         etc
    }

    same for query_params_on_upload

    """

    def __init__(
        self,
        name: str,
        uploader_id: str,
        description: str,
        accepted_file_types: list,
        validator_class: UploaderValidator,
        worker_function: Callable,
        quota_units: int,
        flags: list = None,
        encryptor_class: UploaderEncryptor = None,
        status: str = states.IDLE,
        icon: str = "default.png",
        upload_path: str = None,
        upload_validation_path: str = None,
        quota_validation_path: str = None,
        status_check_path: str = None,
        max_retries: int = 0,
        broker_funcs: Dict[str, List[Callable]] = None,
        query_params_on_validation: dict = None,
        query_params_on_upload: list = [],
        one_event_per_file: bool = False,
        collections_list: list = [envs.MONGO_COLLECTION_DATA_NAME],
        **options,
    ):

        if envs.DEPLOYMENT_SUFFIX is not None:
            name = name + envs.DEPLOYMENT_SUFFIX
            uploader_id = uploader_id + envs.DEPLOYMENT_SUFFIX

        # Passing variables to validator class
        validator_class.uploader_id = uploader_id
        validator_class.quota_units = quota_units
        self.validation_parameters = validator_class.validation_parameters
        # self.encryptor_class = encryptor_class
        self.encryption_parameters = (
            encryptor_class.encryption_parameters if encryptor_class else {}
        )

        self.broker_funcs = broker_funcs
        self.uploader_id = uploader_id
        self.quota_units = quota_units
        self.name = name
        self.description = description
        self.validator_class = validator_class
        self.app_id = envs.APP_ID
        self.one_event_per_file = one_event_per_file

        if worker_function is None:
            self.worker = None
        else:
            self.worker = broker.actor(
                worker_function,
                max_retries=max_retries,
                # hours * seconds * miliseconds
                time_limit=4 * 3600 * 1000,
                actor_name=self.uploader_id,
                queue_name=envs.QUEUE_NAME,
            )

        self.accepted_file_types = accepted_file_types
        self.flags = flags or []
        self.status = status
        self.icon = icon
        self.query_params_on_validation = query_params_on_validation
        self.query_params_on_upload = query_params_on_upload

        # Paths for internal usage
        self.upload_path = upload_path or f"/{self.uploader_id}/files"
        self.upload_validation_path = (
            upload_validation_path or f"/{self.uploader_id}/validation"
        )
        self.quota_validation_path = (
            quota_validation_path or f"/{self.uploader_id}/quota"
        )
        self.status_check_path = status_check_path or f"/{self.uploader_id}/status"

        # Urls for registry service
        self.upload_url = envs.UPLOAD_URL + self.upload_path
        self.upload_validation_url = envs.UPLOAD_URL + self.upload_validation_path
        self.quota_validation_url = envs.UPLOAD_URL + self.quota_validation_path
        self.status_check_url = envs.UPLOAD_URL + self.status_check_path

        self.options = options
        self.collections_list = collections_list

        self.uploader_vars = vars(self)

    def register_uploader(self):
        response, status_code = register_uploader(**self.uploader_vars)
        if status_code != 200:
            raise Exception("Uploader can't register to registry service")
        return response, status_code

    @history.log
    def validate_filenames(self, flask_request: Request):
        """Validate file names provided by user"""

        response, status_code = self.validator_class.get_filenames_response(
            flask_request
        )

        if status_code == 200:
            quota_response, quota_status_code = self.validator_class.calculate_quota(
                flask_request, update_quota_units=False
            )
            if quota_status_code != 200:
                return quota_response, quota_status_code

        return response, status_code

    def get_filepaths(self, event: dict, flask_request: Request):

        response, status_code = self.validator_class.get_file_objects_response(
            flask_request
        )
        if status_code != 200:
            notify_upload_status(event, status=states.IDLE)
            return response, status_code

        quota_response, quota_status_code = self.validator_class.calculate_quota(
            flask_request
        )
        if quota_status_code != 200:
            notify_upload_status(event, status=states.IDLE)
            return quota_response, quota_status_code

        valid_filepaths = (
            self.validator_class.get_only_valid_filepaths_from_objects_response(
                response
            )
        )
        if not valid_filepaths:
            return {"status": states.FAILED, "message": "No valid files provided"}, 400

        return {
            "status": states.SUCCESS,
            "response": response,
            "filepaths": valid_filepaths,
        }, 200

    def get_failed_validation_response(
        self, fp, tenant_id, event_id, serialized_flask_request
    ):

        events = [
            {
                "tenant_id": tenant_id,
                "uploader_id": self.uploader_id,
                "event_id": event_id,
                "filepaths": [],
                "flask_request": serialized_flask_request,
                "validation_response": fp,
            }
        ]

        return {
            "status": fp["status"],
            "message": fp["message"],
            "validation": fp["validation"],
            "event_data": events,
        }, 400

    def get_quota_exceeded_response(
        self, fp, tenant_id, event_id, serialized_flask_request
    ):

        events = [
            {
                "tenant_id": tenant_id,
                "uploader_id": self.uploader_id,
                "event_id": event_id,
                "filepaths": [],
                "flask_request": serialized_flask_request,
                "validation_response": fp,
            }
        ]

        return {
            "status": fp["status"],
            "message": fp["message"],
            "validation": fp,
            "event_data": events,
            **fp,
        }, 402

    @history.log
    def upload_files(self, flask_request: Request, event_id: str = None):
        """Validate file content provided by user and send files for processing if they are valid"""

        tenant_id = flask_request.headers.get("TenantId")
        serialized_flask_request = get_flask_request_dict(flask_request)

        if envs.DESKTOP_ENVIRONMENT and tenant_id is None:
            tenant_id = envs.DESKTOP_TENANT_ID

        event = {
            "tenant_id": tenant_id,
            "uploader_id": self.uploader_id,
            "event_id": event_id,
        }
        notify_upload_status(event, status=states.RUNNING)

        # Preparing and sending the event to worker for background processing
        fp, status = self.get_filepaths(event, flask_request)

        if status == 400:
            return self.get_failed_validation_response(
                fp, tenant_id, event_id, serialized_flask_request
            )
        if status == 402:
            return self.get_quota_exceeded_response(
                fp, tenant_id, event_id, serialized_flask_request
            )

        if self.one_event_per_file:
            events = [
                {
                    "tenant_id": tenant_id,
                    "uploader_id": self.uploader_id,
                    "event_id": event_id,
                    "filepaths": [filepath],
                    "flask_request": serialized_flask_request,
                    "validation_response": fp["response"],
                }
                for filepath in fp["filepaths"]
            ]
            [
                self.worker.send(event)
                for event in events
                if validate_event(event, raise_error=False)
            ]
            return {
                "status": states.SUCCESS,
                "message": "Event sent",
                "event_data": events,
            }, 200
        else:
            event.update(
                {
                    "filepaths": fp["filepaths"],
                    "flask_request": serialized_flask_request,
                    "validation_response": fp["response"],
                }
            )

            if not validate_event(event, raise_error=False):
                log.error(event)
                notify_upload_status(event, status=states.IDLE)
                return {
                    "status": states.FAILED,
                    "message": "Event not valid",
                    "event_data": [event],
                }, 400

            log.info("Sending event: " + str(event))
            self.worker.send(event)

            return {
                "status": states.SUCCESS,
                "message": "Event sent",
                "event_data": [event],
            }, 200

    def init_tenant_quota(self, tenant_id: str, auth_token: str):

        # Used in app_activation_path

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units,
        )

        response, status_code = q.init_quota()

        return response, status_code

    def check_tenant_quota(self, tenant_id: str, auth_token: str):

        # Used for uploader_id/quota route

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units,
        )

        response, status_code = q.check_quota()

        return response, status_code
