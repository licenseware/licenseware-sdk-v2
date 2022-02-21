import os
import pandas as pd
from typing import List
from flask import Request
from flask import send_from_directory
from licenseware.report_builder import ReportBuilder
from licenseware.common.constants import states, envs
from licenseware.utils.logger import log

from .download_xlsx import download_as_xlsx

file_type_mapper = {
    'xlsx': download_as_xlsx,
}


def download_all(file_type: str, report: ReportBuilder, tenant_id: str, filename: str, flask_request: Request):
    if file_type not in file_type_mapper:
        return {
                   'status': states.FAILED,
                   'message': f'Download for file type {file_type} is not supported yet'
               }, 400

    # TODO if more file types are added move this in another func
    if file_type == 'xlsx':

        download_func = file_type_mapper[file_type]

        dirpath = envs.get_tenant_upload_path(tenant_id)
        if not os.path.exists(dirpath): os.makedirs(dirpath)
        filepath = os.path.join(dirpath, filename)

        xlwriter = pd.ExcelWriter(filepath)

        for comp in report.components:
            comp_data = comp.get_data(flask_request)
            comp_df = download_func(
                data=comp_data,
                tenant_id=tenant_id,
                send_file=False
            )

            comp_df.to_excel(xlwriter, sheet_name=comp.title, index=False)

        xlwriter.save()
        xlwriter.close()

        return send_from_directory(
            directory=dirpath,
            path=filename,
            as_attachment=True
        )
