"""
Here add dataclasses for commun data used in the app

Data like:
- environment variables and varabiles based on them;
- different states, running, idle etc;
etc

"""

from licenseware.utils.logger import log

from .filters import filters
from .flags import flags
from .icons import icons
from .states import states

try:
    from .envs import envs
except Exception as err:
    log.warning(err)
