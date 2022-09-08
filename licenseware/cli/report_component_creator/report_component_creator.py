import os
from dataclasses import dataclass

from licenseware.cli.base_creator import BaseCreator
from licenseware.cli.report_component_creator import templates


@dataclass
class paths:
    report_components: str = "./app/report_components"
    root: str = "./"


class ReportComponentCreator(BaseCreator):
    def __init__(self, component_id: str, component_type: str) -> None:
        self.component_id = component_id
        self.component_type = component_type
        super().__init__(component_id)

    def add_report_component_import(self):

        app_init_path = "./app/__init__.py"

        import_component_str = f"from app.report_components.{self.entity_underscore} import {self.entity_underscore}_component"
        register_component_str = (
            f"App.register_report_component({self.entity_underscore}_component)"
        )

        with open(app_init_path, "r") as f:
            data = f.readlines()

        # Importing component
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 1,
            import_component_str,
        )
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 2, "\n"
        )

        # Registering component
        data.insert(data.index(")\n") + 1, register_component_str)
        data.insert(data.index(")\n") + 2, "\n")

        data = "".join(data)

        with open(app_init_path, "w") as f:
            f.write(data)

    def create(self):

        files = ["__init__.py", "report_component.py"]
        filepath = os.path.join(paths.report_components, self.entity_underscore)

        if not os.path.exists(filepath):
            self.add_report_component_import()

        for file in files:
            self.create_file(
                filename=file,
                filepath=filepath,
                template_resource=templates,
                component_type=self.component_type,
            )
