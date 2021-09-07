import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template



def _create_uploader_init_file(path:str, name:str):
    
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader__init___.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=name)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    
    
    
def _create_uploader_worker_file(path:str, name:str):
                
    file_path = os.path.join(path, 'worker.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader_worker.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=name)
    
        with open(file_path, 'w') as f:
            f.write(file_contents)




def _create_uploader_validator_file(path:str, name:str):
    
    file_path = os.path.join(path, 'validator.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader_validator.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=name)
    
        with open(file_path, 'w') as f:
            f.write(file_contents)




def create_uploader(name:str):
    
    if not os.path.exists(os.path.join(app_path, 'uploaders')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'uploaders', name)
    if not os.path.exists(path): os.makedirs(path)
         
    _create_uploader_init_file(path, name)
    _create_uploader_worker_file(path, name)
    _create_uploader_validator_file(path, name)
         