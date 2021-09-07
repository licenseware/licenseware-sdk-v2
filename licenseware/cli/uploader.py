import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template



def _create_uploader_init_file(path:str, uploader_id:str):
    
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader__init___.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    
    
    
def _create_uploader_worker_file(path:str, uploader_id:str):
                
    file_path = os.path.join(path, 'worker.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader_worker.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)
    
        with open(file_path, 'w') as f:
            f.write(file_contents)




def _create_uploader_validator_file(path:str, uploader_id:str):
    
    file_path = os.path.join(path, 'validator.py')
    if not os.path.exists(file_path):
        
        raw_contents = pkg_resources.read_text(resources, 'uploader_validator.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)
    
        with open(file_path, 'w') as f:
            f.write(file_contents)


def _add_uploader_import_to_app_init_file(uploader_id:str):
    
    import_uploader_str   = f'from app.uploaders.{uploader_id} import {uploader_id}_uploader'
    register_uploader_str = f'App.register_uploader({uploader_id}_uploader)'
    
    app_init_path = os.path.join(app_path, '__init__.py')
    
    with open(app_init_path, 'r') as f:
        data = f.readlines()
        
    # Importing uploader 
    data.insert(4, import_uploader_str)
    data.insert(5, '\n')

    # Registering uploader
    data.insert(-1, register_uploader_str)
    data.insert(-1, '\n')
    
    data = "".join(data)
    
    with open(app_init_path, 'w') as f:
        f.write(data)




def create_uploader(uploader_id:str):
    
    if not os.path.exists(os.path.join(app_path, 'uploaders')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'uploaders', uploader_id)
    if not os.path.exists(path): os.makedirs(path)
         
    _create_uploader_init_file(path, uploader_id)
    _create_uploader_worker_file(path, uploader_id)
    _create_uploader_validator_file(path, uploader_id)
    _add_uploader_import_to_app_init_file(uploader_id)
         