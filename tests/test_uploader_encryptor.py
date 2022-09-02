import os
import shutil
import unittest

from licenseware.uploader_encryptor import UploaderEncryptor
from licenseware.utils.aes import AESCipher

# python3 -m unittest tests/test_uploader_encryptor.py


class TestUploaderEncryptor(unittest.TestCase):
    def test_aws_chipher(self):

        password = "secret"
        text_to_encrypt = "hello john"

        aes = AESCipher(password)

        encrypted_text = aes.encrypt(text_to_encrypt)
        decrypted_text = aes.decrypt(encrypted_text)

        self.assertNotEqual(text_to_encrypt, encrypted_text)
        self.assertEqual(text_to_encrypt, decrypted_text)

    def test_encrypt_decrypt_filepath(self):

        filepath = "test_filesSECRET/LMS_OPTIONS_SECRET.csv"

        ue = UploaderEncryptor(filepaths=["SECRET"])

        encfp = ue.encrypt_filepath(filepath)
        decfp = ue.decrypt_filepath(encfp)

        self.assertNotEqual(filepath, encfp)
        self.assertEqual(filepath, decfp)

    def test_encrypt_decrypt_multiple_filepath(self):

        filepath = "test_files/rl/deviceName_database_version.csv"

        ue = UploaderEncryptor(filepaths=["deviceName", "database"])

        encfp = ue.encrypt_filepath(filepath)
        decfp = ue.decrypt_filepath(encfp)

        self.assertNotEqual(filepath, encfp)
        self.assertEqual(filepath, decfp)

    def test_encrypt_decrypt_regex_filepath(self):

        filepath = "test_files/LMS_OPTIONS_SECRET.csv"

        ue = UploaderEncryptor(filepaths=["LMS_OPTIONS_(.*?).csv"])

        encfp = ue.encrypt_filepath(filepath)
        decfp = ue.decrypt_filepath(encfp)

        self.assertNotEqual(filepath, encfp)
        self.assertEqual(filepath, decfp)

    def test_encrypt_decrypt_filepaths(self):

        # Init

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
            columns=[
                "DB_NAME",
                "MACHINE_ID",
                "HOST_NAME",
                "INSTANCE_NAME",
                "Host",
                "Device",
            ],
        )

        ue.set_password("password")

        # Encrypt

        encrypted_filepaths = ue.get_encrypted_filepaths(filepaths)
        self.assertEqual(len(filepaths), len(encrypted_filepaths))

        # Decrypt

        decrypted_filepaths = ue.get_decrypted_filepaths(encrypted_filepaths)
        self.assertEqual(len(filepaths), len(decrypted_filepaths))

        # Clean
        shutil.rmtree(decrypted_filepaths[0].split(os.path.sep)[0])
        shutil.rmtree(encrypted_filepaths[0].split(os.path.sep)[0])

    def test_encrypt_decrypt_filecontent(self):

        filepaths = [
            "test_files/LMS_OPTIONS_SECRET.csv",
            "test_files/cpuq.txt",
            "test_files/rl/deviceName_database_version.csv",
            "test_files/rl/deviceName_database_options.csv",
            "test_files/rl/deviceName_database_dba_feature.csv",
        ]

        values_to_encrypt_from_filecontent = [
            "Machine Name=(.+)",
            "System IP Address 1=(.+)",
        ]

        ue = UploaderEncryptor(filecontent=values_to_encrypt_from_filecontent)

        encrypted_filepaths = ue.get_encrypted_filepaths(filepaths)
        self.assertEqual(len(filepaths), len(encrypted_filepaths))

        ue.encrypt_filecontent(encrypted_filepaths)

        with open("test_files_encrypted/cpuq.txt", "r") as f:
            content = f.read()

        self.assertEqual(content.count(ue.start_tag), 5)

        ue.decrypt_filecontent(encrypted_filepaths)

        # Clean
        shutil.rmtree(encrypted_filepaths[0].split(os.path.sep)[0])
