"""

This package is reponsible for updating the quota per `user_id` at each upload.

Usage:

```py

from licenseware.quota import Quota

q = Quota(tenant_id, uploader_id)
res, status_code = q.init_quota()
res, status_code = q.update_quota(units=1)
res, status_code = q.check_quota(units=1)


```

"""


from .quota import Quota
