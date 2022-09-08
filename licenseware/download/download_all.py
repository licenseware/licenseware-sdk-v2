import os

import pandas as pd
from flask import Request, send_from_directory

from licenseware.common.constants import envs, states
from licenseware.download.download_xlsx import download_as_xlsx
from licenseware.report_builder import ReportBuilder

file_type_mapper = {
    "xlsx": download_as_xlsx,
}


def download_all(
    file_type: str,
    report: ReportBuilder,
    tenant_id: str,
    filename: str,
    flask_request: Request,
):
    if file_type not in file_type_mapper:
        return {
            "status": states.FAILED,
            "message": f"Download for file type {file_type} is not supported yet",
        }, 400

    # TODO if more file types are added move this in another func
    if file_type == "xlsx":

        download_func = file_type_mapper[file_type]

        dirpath = envs.get_tenant_upload_path(tenant_id)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filepath = os.path.join(dirpath, filename)

        xlwriter = pd.ExcelWriter(filepath)

        for comp in report.components:
            comp_data = comp.get_data(flask_request)
            if comp_data:
                comp_df = download_func(
                    data=comp_data, tenant_id=tenant_id, send_file=False
                )

                comp_df.to_excel(
                    xlwriter, sheet_name=comp.sheet_title[0:30], index=False
                )

        xlwriter.save()
        xlwriter.close()

        return send_from_directory(directory=dirpath, path=filename, as_attachment=True)
