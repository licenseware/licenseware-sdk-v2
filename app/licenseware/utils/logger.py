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

import os, sys, json
from loguru import logger as log
 

_debug = os.getenv('DEBUG', '').lower() == 'true'
_log_level = 'DEBUG' if _debug else 'WARNING'

_log_format = """<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>[ <level>{level}</level> ]
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>
<level>{message}</level>
"""

try:
    log.remove(0)
except:
    pass#No default logger


log.add(
    "app.log", 
    rotation="monthly", 
    level=_log_level, 
    format=_log_format
)

log.add(
    sys.stderr, 
    format=_log_format
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

