import os

from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import generate_id

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template


# not sure why only .py files end up in the wheel
resources_filenames = {
    '_main_example.py': 'main_example.py',
    '_main.py': 'main.py',
    '_mock_server.py': 'mock_server.py',
    '_setup.py': 'setup.py',
    '_docker_compose_mongo_redis.py': 'docker-compose-mongo-redis.yml',
    '_env_file.py': '.env',
    '_gitignore_file.py': '.gitignore',
    '_makefile_file.py': 'makefile',
    '_README.md_file.py': 'README.md',
    '_requirements.txt_file.py': 'requirements.txt',
 }
     
     
     
def create_root_files(app_id:str):
    
    personal_suffix = generate_id(3)
    
    for rname, fname in resources_filenames.items():  
        if not os.path.exists(fname):
            raw_contents = pkg_resources.read_text(resources, rname)
            tmp = Template(raw_contents)
            
            file_contents = tmp.render(app_id=app_id, personal_suffix=personal_suffix)
            
            with open(fname, 'w') as f:
                f.write(file_contents)
