import importlib.resources as pkg_resources
import os
from typing import List

from jinja2 import Template

from licenseware.cli.app_pkg_creator import templates

pkg_path = "./app"

pkg_dirs = [
    "common",
    "services",
    "reports",
    "report_components",
    "uploaders",
    "utils",
    "controllers",
    "serializers",
]


class AppPackageCreator:
    def create_pkg_dirs(self):

        created_paths = []
        for name in pkg_dirs:
            path = os.path.join(pkg_path, name)
            if not os.path.exists(path):
                os.makedirs(path)
            created_paths.append(path)

        return created_paths

    def create_init_blank_files(self, created_paths: List[str]):

        for path in created_paths:
            file_path = os.path.join(path, "__init__.py")
            if os.path.exists(file_path):
                continue
            with open(file_path, "w") as f:
                f.write("# Add imports here")

    def create_pkg_init_file(self):
        file_path = os.path.join(pkg_path, "__init__.py")
        if os.path.exists(file_path):
            return
        raw_contents = pkg_resources.read_text(templates, "app__init__.py.jinja")
        file_contents = Template(
            raw_contents, trim_blocks=True, lstrip_blocks=True
        ).render()
        with open(file_path, "w") as f:
            f.write(file_contents)

    @classmethod
    def create(cls):
        created_paths = cls().create_pkg_dirs()
        cls().create_init_blank_files(created_paths)
        cls().create_pkg_init_file()
