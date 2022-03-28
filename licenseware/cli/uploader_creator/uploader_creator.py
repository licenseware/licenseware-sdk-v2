from asyncore import file_dispatcher
from importlib.resources import path
import os
from dataclasses import dataclass
from licenseware.cli.base_creator import BaseCreator
from . import templates



@dataclass
class paths:
    uploaders: str = './app/uploaders',
    root: str = "./"



class UploaderCreator(BaseCreator):

    def __init__(self, uploader_id: str):
        super().__init__(uploader_id)
        

    def create_init_file(self):
        
        self.create_file(
            filename='__init__.py',
            filepath=paths.uploaders


        )


    def create(self):

        self.create_init_file()
        