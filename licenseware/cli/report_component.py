import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template



def _create_component_init_file(path:str, component_id: str, component_type: str):
    
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path): 
        
        raw_contents = pkg_resources.read_text(resources, 'report_component__init__.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(
            component_id=component_id, 
            component_type=component_type
        )
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    
    

def _create_component_file(path:str, component_id: str):
    
    file_path = os.path.join(path, f'{component_id}.py')
    if not os.path.exists(file_path): 
        
        raw_contents = pkg_resources.read_text(resources, 'report_component.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(component_id=component_id)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    


def create_report_component(component_id: str, component_type: str):
    
    if not os.path.exists(os.path.join(app_path, 'report_components')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'report_components', component_id)
    if not os.path.exists(path): os.makedirs(path)
        
    _create_component_init_file(path, component_id, component_type)
    _create_component_file(path, component_id)
    