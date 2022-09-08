from typing import List

from licenseware.common.constants import states
from licenseware.download.download_csv import download_as_csv
from licenseware.download.download_json import download_as_json
from licenseware.download.download_xlsx import download_as_xlsx

file_type_mapper = {
    "json": download_as_json,
    "xlsx": download_as_xlsx,
    "csv": download_as_csv,
}


def download_as(file_type: str, data: List[dict], tenant_id: str, filename: str = None):
    if file_type in file_type_mapper:
        return file_type_mapper[file_type](data, tenant_id, filename)

    return {
        "status": states.FAILED,
        "message": f"Download for file type {file_type} is not supported yet",
    }, 400
