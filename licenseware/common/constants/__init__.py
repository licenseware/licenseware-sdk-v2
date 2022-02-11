"""
Here add dataclasses for commun data used in the app

Data like:
- environment variables and varabiles based on them;
- different states, running, idle etc;
etc

"""

from licenseware.utils.logger import log

from .flags import flags
from .states import states
from .icons import icons
from .filters import filters

try:
    from .envs import envs
except Exception as err: 
    log.warning(err)