import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template



def _create_component_init_file(path:str, component_id: str, component_type: str):
    
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path): 
        
        raw_contents = pkg_resources.read_text(resources, '_report_component__init__.py')
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
        
        raw_contents = pkg_resources.read_text(resources, '_report_component.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(component_id=component_id)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    


def _add_component_import_to_app_init_file(component_id:str):
    
    import_component_str   = f'from app.report_components.{component_id} import {component_id}_component'
    register_component_str = f'App.register_report_component({component_id}_component)'
    
    app_init_path = os.path.join(app_path, '__init__.py')
    
    with open(app_init_path, 'r') as f:
        data = f.readlines()
        
    # Importing component 
    data.insert(4, import_component_str)
    data.insert(5, '\n')

    # Registering component
    data.insert(-1, register_component_str)
    data.insert(-1, '\n')
    
    data = "".join(data)
    
    with open(app_init_path, 'w') as f:
        f.write(data)



def create_report_component(component_id: str, component_type: str):
    
    if component_type is None:
        component_type = component_id.split('_')[-1]
    
    if not os.path.exists(os.path.join(app_path, 'report_components')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'report_components', component_id)
    if not os.path.exists(path): os.makedirs(path)
        
    _create_component_init_file(path, component_id, component_type)
    _create_component_file(path, component_id)
    _add_component_import_to_app_init_file(component_id)
    