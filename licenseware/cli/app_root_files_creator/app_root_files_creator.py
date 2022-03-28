from licenseware.cli.base_creator import BaseCreator
from . import templates


root_files = [
    'gitignore',
    'main.py',
    'README.md',
    'requirements.txt',
    'tox.ini',
    'version.txt',
    'CHANGELOG.md',
    'setup.py',
    'requirements-dev.txt',
    'requirements-tests.txt'
]


class AppRootFilesCreator(BaseCreator):

    def __init__(self, app_id: str):
        super().__init__(app_id)


    def create(self):

        for file in root_files:    

            filename = file if file not in ['gitignore'] else '.' + file

            self.create_file(
                filename=filename,
                filepath='./',
                template_filename=file + '.jinja',
                template_resource=templates
            )