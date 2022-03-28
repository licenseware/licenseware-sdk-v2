import os
from types import ModuleType
from jinja2 import Template
import importlib.resources as pkg_resources
from abc import ABCMeta, abstractmethod



class BaseCreator(metaclass=ABCMeta):

    def __init__(self, app_id: str):
        app_idli = app_id.strip().replace("-", "|").replace("_", "|").split("|")
        self.app_title = "".join([v.capitalize() for v in app_idli]) # odb-service => OdbService
        self.app_dash = "-".join([v.lower() for v in app_idli]) # odb-service => odb-service
        self.app_dash_upper = "-".join([v.upper() for v in app_idli]) # odb-service => ODB-SERVICE
        self.app_underscore = "_".join([v.lower() for v in app_idli]) # odb-service => odb_service
        self.app_underscore_upper = "_".join([v.upper() for v in app_idli]) # odb-service => ODB_SERVICE


    @classmethod
    def __subclasshook__(cls, subclass):
        # Ensure `create` method is provided
        return (
            hasattr(subclass, 'create') and callable(subclass.create)
            # Fail
            or NotImplemented
        )

    @abstractmethod
    def create(self):
        raise NotImplemented

    def create_file(
        self, 
        filename: str, 
        filepath: str, 
        template_resource: ModuleType, 
        template_filename: str = None, 
        **template_vars
    ):

        file_path = os.path.join(filepath, filename)
        if os.path.exists(file_path): return

        raw_contents = pkg_resources.read_text(template_resource, template_filename or filename + '.jinja')
        file_contents = Template(raw_contents).render(
            **{
                'app_title': self.app_title, 
                'app_dash': self.app_dash,
                'app_dash_upper': self.app_dash_upper,
                'app_underscore': self.app_underscore,
                'app_underscore_upper': self.app_underscore_upper
            }, **template_vars
        )

        with open(file_path, 'w') as f:
            f.write(file_contents)