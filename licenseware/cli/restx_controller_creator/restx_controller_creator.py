import os
from dataclasses import dataclass

from licenseware.cli.base_creator import BaseCreator
from licenseware.cli.restx_controller_creator import templates


@dataclass
class paths:
    controllers: str = "./app/controllers"
    root: str = "./"


class RestxControllerCreator(BaseCreator):
    def __init__(self, controller_name: str):
        super().__init__(controller_name)

    def add_namespace_import(self):

        app_init_path = "./app/__init__.py"

        import_controller_str = f"from app.controllers.{self.entity_underscore}_controller import ns as {self.entity_underscore}_ns"
        register_controller_str = f"App.register_namespace({self.entity_underscore}_ns)"

        with open(app_init_path, "r") as f:
            data = f.readlines()

        # Importing controller
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 1,
            import_controller_str,
        )
        data.insert(
            data.index("from licenseware.app_builder import AppBuilder\n") + 2, "\n"
        )

        # Registering controller
        data.insert(data.index(")\n") + 1, register_controller_str)
        data.insert(data.index(")\n") + 2, "\n")

        data = "".join(data)

        with open(app_init_path, "w") as f:
            f.write(data)

    def create(self):

        filepath = os.path.join(
            paths.controllers, self.entity_underscore + "_controller.py"
        )

        if not os.path.exists(filepath):
            self.add_namespace_import()

        self.create_file(
            filename=self.entity_underscore + "_controller.py",
            filepath=paths.controllers,
            template_filename="restx_controller.py.jinja",
            template_resource=templates,
        )
