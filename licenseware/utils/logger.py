"""

Docs: 
https://github.com/Delgan/loguru


Basic functionality:

from loguru import logger

log._debug("Debug log")
log.info("Info log")
log.success("Success log")
log.warning("Warning log")
log.error("Error log")
log.critical("Critical log")

try:
    raise Exception("Demo exception")
except:
    log.exception("Exception log")
    log.trace("Trace log")


datetime | level | module_name:function_name:line - message

2021-05-27 10:00:35.276 | DEBUG    | m1:testm1:8 - Debug log
2021-05-27 10:00:35.277 | INFO     | m1:testm1:9 - Info log
2021-05-27 10:00:35.277 | SUCCESS  | m1:testm1:10 - Success log
2021-05-27 10:00:35.277 | WARNING  | m1:testm1:11 - Warning log
2021-05-27 10:00:35.278 | ERROR    | m1:testm1:12 - Error log
2021-05-27 10:00:35.278 | CRITICAL | m1:testm1:13 - Critical log
2021-05-27 10:00:35.278 | ERROR    | m1:testm1:18 - Exception log
Traceback (most recent call last):

  File "main.py", line 30, in <module>
    testm1()
    └ <function testm1 at 0x7f1ece69db80>

> File "/home/acmt/Documents/licenseware-sdk/logs/m1.py", line 16, in testm1
    raise Exception("Demo exception")

Exception: Demo exception


To see log colors in docker logs add the following in docker-compose file:

tty: true
environment:
    - 'TERM=xterm-256color'


"""

import contextlib
import json
import os
import sys

from loguru import logger as log

try:
    from flask import has_request_context, request

    outside_flask = False
except Exception:
    print("Outside flask context")
    outside_flask = True

_debug = bool(os.getenv("DEBUG", ""))
_log_level = os.getenv("LOG_LEVEL", "INFO").upper() if not _debug else "DEBUG"

if "local" in os.getenv("ENVIRONMENT", "local").lower():
    _log_format = """<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>[ <level>{level}</level> ]
    <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>
    <level>{message}</level>
    """
else:
    _log_format = "[{level}] [----- {name}:{function}:{line} -----]    [+++++ METADATA: {extra} +++++]    [***** MESSAGE: {message}\n"

with contextlib.suppress(ValueError):
    log.remove(0)
log.add(sys.stderr, format=_log_format, level=_log_level)


class Placeholder(dict):  # HACK: to avoid `str.format_map` error on missing keys
    def __missing__(self, key):
        return str(key)


CRITICALS = [
    "password",
    "new_password",
    "old_password",
]


def _get_payload(json_payload):
    if not isinstance(json_payload, dict):
        return {}
    for key, value in json_payload.items():
        if key not in CRITICALS:
            yield key, value


if not outside_flask:
    log.configure(
        patcher=lambda record: record["extra"].update(
            tenant_id=request.headers.get("Tenantid"),
            host=request.headers.get("Host"),
            user_agent=request.headers.get("User-Agent"),
            accept=request.headers.get("Accept"),
            content_type=request.headers.get("Content-Type"),
            request_url=request.url,
            request_method=request.method,
            json_payload=dict(_get_payload(request.get_json()))
            if request.get_json()
            else None,
            multiform_payload=request.files if request.files else None,
        )
        if has_request_context()
        else None,
        extra=Placeholder(),
    )

# Pretty logs for dict data
log_dict = lambda dict_: log.info(json.dumps(dict_, indent=4, sort_keys=True))

## Test
# log.debug("Debug log")
# log.info("Info log")
# log.success("Success log")
# log.warning("Warning log")
# log.error("Error log")
# log.critical("Critical log")

# try:
#     raise Exception("Demo exception")
# except:
#     log.exception("Exception log")
#     log.trace("Trace log")
