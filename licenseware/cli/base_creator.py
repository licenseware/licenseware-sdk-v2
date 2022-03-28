import os
from types import ModuleType
from jinja2 import Template
import importlib.resources as pkg_resources
from abc import ABCMeta, abstractmethod



class BaseCreator(metaclass=ABCMeta):

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        entity_idli = entity_id.strip().replace("-", "|").replace("_", "|").split("|")
        self.entity_title = "".join([v.capitalize() for v in entity_idli]) # odb-service => OdbService
        self.entity_dash = "-".join([v.lower() for v in entity_idli]) # odb-service => odb-service
        self.entity_dash_upper = "-".join([v.upper() for v in entity_idli]) # odb-service => ODB-SERVICE
        self.entity_underscore = "_".join([v.lower() for v in entity_idli]) # odb-service => odb_service
        self.entity_underscore_upper = "_".join([v.upper() for v in entity_idli]) # odb-service => ODB_SERVICE


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
                'entity_title': self.entity_title, 
                'entity_dash': self.entity_dash,
                'entity_dash_upper': self.entity_dash_upper,
                'entity_underscore': self.entity_underscore,
                'entity_underscore_upper': self.entity_underscore_upper
            }, **template_vars
        )

        with open(file_path, 'w') as f:
            f.write(file_contents)