import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template



def _create_report_init_file(path:str, report_id:str):
    
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):         
        
        raw_contents = pkg_resources.read_text(resources, 'report__init__.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(report_id=report_id)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    
    

def _create_report_file(path:str, report_id:str):
    
    file_path = os.path.join(path, f'{report_id}.py')
    if not os.path.exists(file_path):         
        
        raw_contents = pkg_resources.read_text(resources, 'report.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(report_id=report_id)
        
        with open(file_path, 'w') as f:
            f.write(file_contents)
    


def create_report(report_id:str):
    
    if not os.path.exists(os.path.join(app_path, 'reports')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'reports', report_id)
    if not os.path.exists(path): os.makedirs(path)
         
    _create_report_init_file(path, report_id)
    _create_report_file(path, report_id)
         