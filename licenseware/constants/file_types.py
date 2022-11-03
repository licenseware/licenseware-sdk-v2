from dataclasses import dataclass

from .base_enum import BaseEnum


@dataclass(frozen=True)
class FileTypes:
    XLS: str = ".xls"
    XLSX: str = ".xlsx"
    CSV: str = ".csv"
    TXT: str = ".txt"
    XML: str = ".xml"
    ZIP: str = ".zip"
    TAR: str = ".tar"
    TAR_BZ2: str = ".tar.bz2"
    TAR_GZ: str = ".tar.gz"
    TGZ: str = ".tgz"
    GENERIC_EXCEL: tuple = (XLS, XLSX)
    GENERIC_ARCHIVE: tuple = (ZIP, TAR, TAR_BZ2, TAR_GZ, TGZ)


class DownloadFileType(BaseEnum):
    JSON = "json"
    XLSX = "xlsx"
    CSV = "csv"
