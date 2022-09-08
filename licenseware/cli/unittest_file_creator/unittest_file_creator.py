import os

from licenseware.cli.base_creator import BaseCreator
from licenseware.cli.unittest_file_creator import templates


class UnittestFileCreator(BaseCreator):
    def __init__(self, app_id: str):
        super().__init__(app_id)

    def create(self):

        testfiles_path = f"test_files/{self.entity_underscore}"

        if not os.path.exists(testfiles_path):
            os.makedirs(testfiles_path)

        fname = "test_" + self.entity_underscore + ".py"

        if not os.path.exists(os.path.join("./tests", fname)):
            self.create_file(
                filename=fname,
                filepath="./tests",
                template_filename="test_name.py.jinja",
                template_resource=templates,
            )
