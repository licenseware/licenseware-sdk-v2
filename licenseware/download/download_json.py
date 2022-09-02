import json
import os
from typing import List

from flask import send_from_directory

from licenseware.common.constants import envs


def download_as_json(data: List[dict], tenant_id: str, filename: str = None):

    if filename is None:
        filename = "data.json"
    if not filename.endswith("json"):
        filename = filename + ".json"

    dirpath = envs.get_tenant_upload_path(tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, filename)
    with open(filepath, "w") as outfile:
        json.dump(data, outfile)

    return send_from_directory(directory=dirpath, path=filename, as_attachment=True)
