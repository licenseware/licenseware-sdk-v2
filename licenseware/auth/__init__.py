"""

Here is the authentification class for machines and services.
Authentification credentials will be taken from `.env` file.

Usage:
```py
from licenseware.auth import Authenticator

Authenticator.connect()
```

`AppBuilder` does the authentification on `init_app()`

"""

from .auth import Authenticator
