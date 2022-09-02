import os
from typing import List

import pandas as pd
from flask import send_from_directory

from licenseware.common.constants import envs


def download_as_xlsx(
    data: List[dict], tenant_id: str, filename: str = None, send_file: bool = True
):

    if filename is None:
        filename = "data.xlsx"
    if not filename.endswith("xlsx"):
        filename = filename + ".xlsx"

    dirpath = envs.get_tenant_upload_path(tenant_id)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    filepath = os.path.join(dirpath, filename)
    try:
        df = pd.DataFrame.from_records(data)
    except ValueError:
        df = pd.DataFrame.from_records([data])

    if not send_file:
        return df

    df.to_excel(filepath, index=False)

    return send_from_directory(directory=dirpath, path=filename, as_attachment=True)
