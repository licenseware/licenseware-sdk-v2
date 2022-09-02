import os
from typing import List

import pandas as pd
from flask import send_from_directory

from licenseware.common.constants import envs


def download_as_csv(data: List[dict], tenant_id: str, filename: str = None):
    if filename is None:
        filename = "data.csv"
    if not filename.endswith("csv"):
        filename = filename + ".csv"

    dirpath = envs.get_tenant_upload_path(tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, filename)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, quotechar='"')

    return send_from_directory(directory=dirpath, path=filename, as_attachment=True)
