import os
from licenseware.utils.logger import log

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template

from .root_files import create_root_files



app_path = './app'
app_dirs = [
    'common',
    'reports',
    'report_components',
    'uploaders',
    'utils',
    'controllers',
    'serializers',
]


boilerplate_filenames = [
    'main.py',
    'mock_server.py',
    'makefile',
    '.env',
    'docker-compose-mongo-redis.yml',
    'requirements.txt',
    'setup.py',
    'README.md',
    'main_example.py',
]
     
     
     
def _create_app_init_file():
    
    file_path = os.path.join(app_path, '__init__.py')
    if not os.path.exists(file_path):

        raw_contents = pkg_resources.read_text(resources, 'app__init__.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render()
        
        with open(file_path, 'w') as f:
            f.write(file_contents)


        
def _create_pkg_init_files(created_paths: list):

    for path in created_paths:
        file_path = os.path.join(path, '__init__.py')         
        if os.path.exists(file_path):
            log.warning("Skipped creating {} because it already exists")
            continue
        with open(file_path, 'w') as f:
            f.write("# Add imports here")
     



def create_app_dirs():
    
    created_paths = []
    for dir_name in app_dirs:
        path = os.path.join(app_path, dir_name)
        if not os.path.exists(path): os.makedirs(path)
        created_paths.append(path)
        
    _create_pkg_init_files(created_paths)
    _create_app_init_file()
    
    create_root_files(*boilerplate_filenames)
    