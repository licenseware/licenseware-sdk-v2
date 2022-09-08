import os
from dataclasses import dataclass

from licenseware.cli.base_creator import BaseCreator
from licenseware.cli.report_creator import templates


@dataclass
class paths:
    reports: str = "./app/reports"
    root: str = "./"


class ReportCreator(BaseCreator):
    def __init__(self, report_id: str):
        super().__init__(report_id)

    def add_report_import(self):

        app_init_path = "./app/__init__.py"

        import_report_str = f"from app.reports.{self.entity_underscore} import {self.entity_underscore}_report"
        register_report_str = f"App.register_report({self.entity_underscore}_report)"

        with open(app_init_path, "r") as f:
            data = f.readlines()

        # Importing report
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 1,
            import_report_str,
        )
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 2, "\n"
        )

        # Registering report
        data.insert(data.index(")\n") + 1, register_report_str)
        data.insert(data.index(")\n") + 2, "\n")

        data = "".join(data)

        with open(app_init_path, "w") as f:
            f.write(data)

    def create(self):

        files = ["__init__.py", "report.py"]
        filepath = os.path.join(paths.reports, self.entity_underscore)

        if not os.path.exists(filepath):
            self.add_report_import()

        for file in files:
            self.create_file(
                filename=file, filepath=filepath, template_resource=templates
            )
