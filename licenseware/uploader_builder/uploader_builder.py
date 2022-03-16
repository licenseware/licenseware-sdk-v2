from typing import Callable
from flask import Request
from licenseware.common.constants import envs, states
from licenseware.registry_service.register_uploader import register_uploader
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log
from licenseware.common.validators import validate_event
from licenseware.quota import Quota
from licenseware.notifications import notify_upload_status
from licenseware.uploader_validator.uploader_validator import UploaderValidator
from licenseware import history


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
            flags: list = [],
            status: str = states.IDLE,
            icon: str = "default.png",
            upload_path: str = None,
            upload_validation_path: str = None,
            quota_validation_path: str = None,
            status_check_path: str = None,
            max_retries: int = 0,
            query_params_on_validation: dict = None,
            query_params_on_upload: dict = None,
            one_event_per_file: bool = False,
            **options
    ):

        if envs.DEPLOYMENT_SUFFIX is not None:
            name = name + envs.DEPLOYMENT_SUFFIX
            uploader_id = uploader_id + envs.DEPLOYMENT_SUFFIX

        # Passing variables to validator class
        validator_class.uploader_id = uploader_id
        validator_class.quota_units = quota_units
        self.validation_parameters = validator_class.validation_parameters

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
                # 1 hour in milliseconds (default is 10 minutes)
                time_limit=3600000,
                actor_name=self.uploader_id,
                queue_name=envs.QUEUE_NAME
            )

        self.accepted_file_types = accepted_file_types
        self.flags = flags
        self.status = status
        self.icon = icon
        self.query_params_on_validation = query_params_on_validation
        self.query_params_on_upload = query_params_on_upload

        # Paths for internal usage
        self.upload_path = upload_path or f"/{self.uploader_id}/files"
        self.upload_validation_path = upload_validation_path or f"/{self.uploader_id}/validation"
        self.quota_validation_path = quota_validation_path or f"/{self.uploader_id}/quota"
        self.status_check_path = status_check_path or f"/{self.uploader_id}/status"

        # Urls for registry service
        self.upload_url = envs.UPLOAD_URL + self.upload_path
        self.upload_validation_url = envs.UPLOAD_URL + self.upload_validation_path
        self.quota_validation_url = envs.UPLOAD_URL + self.quota_validation_path
        self.status_check_url = envs.UPLOAD_URL + self.status_check_path

        self.options = options

        self.uploader_vars = vars(self)

    def register_uploader(self):
        response, status_code = register_uploader(**self.uploader_vars)
        if status_code != 200:
            raise Exception("Uploader can't register to registry service")
        return response, status_code

    @history.log()
    def validate_filenames(self, flask_request: Request):
        """ Validate file names provided by user """

        response, status_code = self.validator_class.get_filenames_response(
            flask_request)

        if status_code == 200:
            quota_response, quota_status_code = self.validator_class.calculate_quota(
                flask_request, update_quota_units=False)
            if quota_status_code != 200: return quota_response, quota_status_code

        return response, status_code

    @history.log()
    def upload_files(self, flask_request: Request, event_id: str = None):
        """ Validate file content provided by user and send files for processing if they are valid """

        header_event_id = flask_request.headers.get("EventId") or event_id
        if header_event_id is None:
            raise Exception("Parameter `EventId` not provided in headers")

        if self.worker is None:
            return {
                       "status": states.FAILED,
                       "message": "Worker function not provided"
                   }, 400

        event = {
            'tenant_id': flask_request.headers.get("Tenantid"),
            'uploader_id': self.uploader_id,
            'event_id': header_event_id
        }
        notify_upload_status(event, status=states.RUNNING)

        response, status_code = self.validator_class.get_file_objects_response(
            flask_request)
        if status_code != 200:
            notify_upload_status(event, status=states.IDLE)
            return response, status_code

        quota_response, quota_status_code = self.validator_class.calculate_quota(
            flask_request)
        if quota_status_code != 200:
            notify_upload_status(event, status=states.IDLE)
            return quota_response, quota_status_code

        valid_filepaths = self.validator_class.get_only_valid_filepaths_from_objects_response(
            response)
        if not valid_filepaths:
            return {'status': states.FAILED, 'message': 'No valid files provided'}, 400

        # Preparing and sending the event to worker for background processing
        flask_headers = dict(
            flask_request.headers) if flask_request.headers else {}
        flask_json = dict(flask_request.json) if flask_request.json else {}
        flask_args = dict(flask_request.args) if flask_request.args else {}

        if self.one_event_per_file:
            events = [
                {
                    'tenant_id': flask_headers.get("Tenantid"),
                    'uploader_id': self.uploader_id,
                    'event_id': header_event_id,
                    'filepaths': [filepath],
                    'flask_request': {**flask_json, **flask_headers, **flask_args},
                    'validation_response': response
                }
                for filepath in valid_filepaths
            ]
            [
                self.worker.send(event) for event in events if validate_event(event, raise_error=False)
            ]
            return {'status': states.SUCCESS, 'message': 'Event sent', 'event_data': events}, 200
        else:
            event.update({
                'filepaths': valid_filepaths,
                'flask_request': {**flask_json, **flask_headers, **flask_args},
                'validation_response': response
            })

            if not validate_event(event, raise_error=False):
                log.error(event)
                notify_upload_status(event, status=states.IDLE)
                return {'status': states.FAILED, 'message': 'Event not valid', 'event_data': event}, 400

            log.info("Sending event: " + str(event))
            self.worker.send(event)

            return {'status': states.SUCCESS, 'message': 'Event sent', 'event_data': [event]}, 200

    def init_tenant_quota(self, tenant_id: str, auth_token: str):

        # Used in app_activation_path

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units
        )

        response, status_code = q.init_quota()

        log.warning(response)
        log.warning(status_code)

        return response, status_code

    def check_tenant_quota(self, tenant_id: str, auth_token: str):

        # Used for uploader_id/quota route

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units
        )

        response, status_code = q.check_quota()

        return response, status_code
