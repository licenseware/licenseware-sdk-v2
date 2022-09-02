import os
import re
import shutil
from typing import Dict, List

import pandas as pd

from licenseware.common.constants import envs
from licenseware.utils.aes import AESCipher


class UploaderEncryptor:

    """

    This class will use AES encryption algorithm to encrypt files given.
    Each parameter receives either a simple string which will be encrypted or a regex string.

    The regex string needs to be grouped:
    Ex:
    ```
        Input: "/Collection-deviceName"
        filepaths: ["Collection-(.+?)"] will return this: "/Collection-iGSS0a9GfPDJ24ni3vfmRSrPIYdY3kFj4-EsRjfz9E0="
    ```

    Params:

    filepaths = ["Collection-(.+?)", "DeviceName"] # this will encrypt the filepath including the filename
    filecontent = ["ODBName(.+?)"] # encrypt text found with regex from file content (csv, txt, xml) replace all
    columns = ["OS", "IP"] # encrypt the entire column data where the specified columns are found (csv, excel with multiple sheets)
    encryption_password = "secret password" # the password that will be used for encrypting and decrypting data
    You can also set password later with `set_password("password")`

    Usage:

    ```py

    from licenseware.uploader_encryptor import UploaderEncrytor

    filepaths = [
        "test_files/RVTools.xlsx",
        "test_files/LMS_OPTIONS_SECRET.csv",
        "test_files/cpuq.txt",
        "test_files/rl/deviceName_database_version.csv",
        "test_files/rl/deviceName_database_options.csv",
        "test_files/rl/deviceName_database_dba_feature.csv",
    ]

    ue = UploaderEncryptor(
        filepaths=["deviceName", "database", "LMS_OPTIONS_(.*?).csv", "rl"],
        filecontent=["Machine Name=(.+)", "System IP Address 1=(.+)"],
        columns=["DB_NAME", "MACHINE_ID", "HOST_NAME", "INSTANCE_NAME", "Host", "Device"]
    )

    ue.set_password("password")

    # Encrypt
    encrypted_filepaths = ue.get_encrypted_filepaths(filepaths)

    # Decrypt
    decrypted_filepaths = ue.get_decrypted_filepaths(encrypted_filepaths)

    ```

    """

    def __init__(
        self,
        filepaths: List[str] = None,
        filecontent: List[str] = None,
        columns: List[str] = None,
        encryption_password: str = None,
    ):

        self.filepaths = filepaths or []
        self.filecontent = filecontent or []
        self.columns = columns or []
        self.encryption_password = encryption_password or "password"
        self.encryption_parameters = self.get_encryption_parameters()
        self.start_tag = "#sc#"
        self.end_tag = "#ec#"
        self.store = None

    def set_password(self, password: str):
        self.encryption_password = password

    def add_tags(self, value: str):
        return self.start_tag + value + self.end_tag

    def rem_tags(self, value: str):
        no_tags_values = re.findall(
            re.compile(f"{self.start_tag}(.*?){self.end_tag}"), value
        )
        return no_tags_values

    def encrypt(self, value: str):
        return self.add_tags(AESCipher(self.encryption_password).encrypt(str(value)))

    def decrypt(self, encrypted_value: str):

        if not isinstance(encrypted_value, str):
            return encrypted_value

        if encrypted_value.startswith(self.start_tag) and encrypted_value.endswith(
            self.end_tag
        ):
            encrypted_value = self.rem_tags(encrypted_value)[0]
        if not encrypted_value.endswith("="):
            encrypted_value = encrypted_value + "="

        return AESCipher(self.encryption_password).decrypt(encrypted_value)

    def get_encryption_parameters(self):
        return dict(
            filepaths=self.filepaths, filecontent=self.filecontent, columns=self.columns
        )

    def encrypt_filepath(self, filepath: str):

        if self.store is None:
            self.store = {}

        encfp = filepath
        for regexpr in self.filepaths:
            values_to_encrypt = set(re.findall(re.compile(regexpr), encfp))
            for val in values_to_encrypt:

                if val not in self.store:

                    encrypted = self.encrypt(val)
                    encfp = encfp.replace(val, encrypted)

                    self.store[val] = {
                        "regexpr": regexpr,
                        "not_encrypted": val,
                        "encrypted": encrypted,
                    }

                else:
                    encfp = encfp.replace(val, self.store[val]["encrypted"])

        return encfp

    def decrypt_filepath(self, filepath: str):

        enc_values = re.findall(
            re.compile(f"{self.start_tag}(.*?){self.end_tag}"), filepath
        )

        encdec = {}
        for encval in enc_values:
            encdec[self.add_tags(encval)] = self.decrypt(encval)

        decfp = filepath
        for enc, dec in encdec.items():
            decfp = decfp.replace(enc, dec)

        return decfp

    def mirror_dirs(self, filepaths_dict: Dict[str, str], enctype: str) -> List[str]:

        assert enctype in ["encrypt", "decrypt"]

        processed_filepaths = []
        for sourcepath, destinationpath in filepaths_dict.items():

            dstdir = os.path.join(envs.FILE_UPLOAD_PATH, f"{enctype}ed")

            dstpathli = [dstdir] + destinationpath.replace(
                envs.FILE_UPLOAD_PATH, ""
            ).split(os.path.sep)[1:]
            dstpath = os.path.join(*dstpathli)

            root_path = os.path.dirname(dstpath)
            if not os.path.exists(root_path):
                os.makedirs(root_path)

            shutil.copy2(sourcepath, dstpath)
            processed_filepaths.append(dstpath)

        return processed_filepaths

    def get_src_dst_files(self, filepaths: List[str], enctype: str):

        assert enctype in ["encrypt", "decrypt"]

        self.store = {}

        encdecfunc = (
            lambda fp: self.encrypt_filepath(fp)
            if enctype == "encrypt"
            else self.decrypt_filepath(fp)
        )

        filepaths_dict = {}
        for fp in filepaths:
            if not os.path.exists(fp):
                continue
            filepaths_dict[fp] = encdecfunc(fp)

        self.store = None

        return filepaths_dict

    def get_encrypted_filepaths(self, filepaths: List[str]):

        encrypted_filepaths_dict = self.get_src_dst_files(filepaths, "encrypt")
        encrypted_filepaths_list = self.mirror_dirs(encrypted_filepaths_dict, "encrypt")
        self.encrypt_filecontent(encrypted_filepaths_list)

        return encrypted_filepaths_list

    def get_decrypted_filepaths(self, filepaths: List[str]):

        decrypted_filepaths_dict = self.get_src_dst_files(filepaths, "decrypt")
        decrypted_filepaths_list = self.mirror_dirs(decrypted_filepaths_dict, "decrypt")
        self.decrypt_filecontent(decrypted_filepaths_list)

        return decrypted_filepaths_list

    def encrypt_non_excel_filecontent(self, filepath: str):

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        to_encrypt_values = set()
        for regexp in self.filecontent:
            matches = re.findall(re.compile(regexp), content)
            if not matches:
                continue
            to_encrypt_values.add(*matches)

        encryption_dict = {}
        for tev in to_encrypt_values:
            encryption_dict[tev] = self.encrypt(tev)

        for val, encval in encryption_dict.items():
            content = re.sub(val, encval, content)

        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)

        return content

    def decrypt_non_excel_filecontent(self, filepath: str):

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        enc_values = re.findall(
            re.compile(f"{self.start_tag}(.*?){self.end_tag}"), content
        )

        encdec = {}
        for encval in enc_values:
            encdec[self.add_tags(encval)] = self.decrypt(encval)

        for encval, val in encdec.items():
            content = re.sub(encval, val, content)

        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)

        return content

    def decrypt_excel_filecontent(self, filepath: str):

        decrypted_dfs = {}
        excel = pd.ExcelFile(filepath)
        for sheet_name in excel.sheet_names:

            df = pd.read_excel(excel, sheet_name)

            for col in self.columns:
                if col not in df.columns:
                    continue

                decryption_dict = {}
                for val in df[col].unique():
                    decryption_dict[val] = self.decrypt(val)

                df[col] = df[col].apply(
                    lambda cell: decryption_dict[cell]
                    if cell in decryption_dict
                    else cell
                )

            decrypted_dfs[sheet_name] = df

        writer = pd.ExcelWriter(filepath)
        for name, df in decrypted_dfs.items():
            df.to_excel(writer, sheet_name=name, index=False)
        writer.save()
        writer.close()

        return filepath

    def decrypt_csv_filecontent(self, filepath: str):

        # TODO - handle big csv's
        df = pd.read_csv(filepath)

        for col in self.columns:
            if col not in df.columns:
                continue

            decryption_dict = {}
            for val in df[col].unique():
                decryption_dict[val] = self.decrypt(val)

            df[col] = df[col].apply(
                lambda cell: decryption_dict[cell] if cell in decryption_dict else cell
            )

        df.to_csv(filepath, index=False)

        return filepath

    def encrypt_excel_filecontent(self, filepath: str):

        encrypted_dfs = {}
        excel = pd.ExcelFile(filepath)
        for sheet_name in excel.sheet_names:

            df = pd.read_excel(excel, sheet_name)

            for col in self.columns:
                if col not in df.columns:
                    continue

                encryption_dict = {}
                for val in df[col].unique():
                    encryption_dict[val] = self.encrypt(val)

                df[col] = df[col].apply(
                    lambda cell: encryption_dict[cell]
                    if cell in encryption_dict
                    else cell
                )

            encrypted_dfs[sheet_name] = df

        writer = pd.ExcelWriter(filepath)
        for name, df in encrypted_dfs.items():
            df.to_excel(writer, sheet_name=name, index=False)
        writer.save()
        writer.close()

        return filepath

    def encrypt_csv_filecontent(self, filepath: str):

        # TODO - handle big csv's
        df = pd.read_csv(filepath)

        for col in self.columns:
            if col not in df.columns:
                continue

            encryption_dict = {}
            for val in df[col].unique():
                encryption_dict[val] = self.encrypt(val)

            df[col] = df[col].apply(
                lambda cell: encryption_dict[cell] if cell in encryption_dict else cell
            )

        df.to_csv(filepath, index=False)

        return filepath

    def encrypt_filecontent(self, filepaths: List[str]):

        for fp in filepaths:
            if fp.endswith(
                (
                    ".txt",
                    ".xml",
                    ".csv",
                )
            ):
                self.encrypt_non_excel_filecontent(fp)
            elif (
                fp.endswith(
                    (
                        ".xls",
                        ".xlsx",
                    )
                )
                and self.columns
            ):
                self.encrypt_excel_filecontent(fp)
            elif fp.endswith(".csv") and self.columns:
                self.encrypt_csv_filecontent(fp)

        return filepaths

    def decrypt_filecontent(self, filepaths: List[str]):

        for fp in filepaths:
            if fp.endswith(
                (
                    ".txt",
                    ".xml",
                    ".csv",
                )
            ):
                self.decrypt_non_excel_filecontent(fp)
            elif fp.endswith(".csv") and self.columns:
                self.decrypt_csv_filecontent(fp)
            elif (
                fp.endswith(
                    (
                        ".xls",
                        ".xlsx",
                    )
                )
                and self.columns
            ):
                self.decrypt_excel_filecontent(fp)

        return filepaths
