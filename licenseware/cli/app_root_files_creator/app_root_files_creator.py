from licenseware.cli.app_root_files_creator import templates
from licenseware.cli.base_creator import BaseCreator

root_files = [
    "gitignore",
    "ignoretests",
    "main.py",
    "README.md",
    "requirements.txt",
    "tox.ini",
    "pytest.ini",
    "version.txt",
    "CHANGELOG.md",
    "setup.py",
    "requirements-dev.txt",
]


class AppRootFilesCreator(BaseCreator):
    def __init__(self, app_id: str):
        super().__init__(app_id)

    def create(self):

        for file in root_files:

            filename = file if file not in ["ignoretests", "gitignore"] else "." + file

            self.create_file(
                filename=filename,
                filepath="./",
                template_filename=file + ".jinja",
                template_resource=templates,
            )
