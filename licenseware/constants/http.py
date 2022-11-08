from http import HTTPStatus

HTTP_METHODS = {"GET", "PUT", "POST", "DELETE"}
HTTP_STATUS_CODES = set([item.value for item in HTTPStatus])
