import os
from dataclasses import dataclass

from licenseware.cli.base_creator import BaseCreator
from licenseware.cli.uploader_creator import templates


@dataclass
class paths:
    uploaders: str = "./app/uploaders"
    root: str = "./"


class UploaderCreator(BaseCreator):
    def __init__(self, uploader_id: str):
        super().__init__(uploader_id)

    def add_uploader_import(self):

        app_init_path = "./app/__init__.py"

        with open(app_init_path, "r") as f:
            data = f.readlines()

        import_uploader_str = f"from app.uploaders.{self.entity_underscore} import {self.entity_underscore}_uploader"
        register_uploader_str = (
            f"App.register_uploader({self.entity_underscore}_uploader)"
        )

        # Importing uploader
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 1,
            import_uploader_str,
        )
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 2, "\n"
        )

        # Registering uploader
        data.insert(data.index(")\n") + 1, register_uploader_str)
        data.insert(data.index(")\n") + 2, "\n")

        data = "".join(data)

        with open(app_init_path, "w") as f:
            f.write(data)

    def create(self):

        files = ["__init__.py", "validator.py", "worker.py", "encryptor.py"]
        filepath = os.path.join(paths.uploaders, self.entity_underscore)

        if not os.path.exists(filepath):
            self.add_uploader_import()

        for file in files:
            self.create_file(
                filename=file, filepath=filepath, template_resource=templates
            )
