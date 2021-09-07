import os
from .app_dirs import app_path, create_app_dirs



def create_report_component(name:str):
    
    if not os.path.exists(os.path.join(app_path, 'report_components')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'report_components', name)
    if not os.path.exists(path): os.makedirs(path)
        
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path): 
        with open(file_path, 'w') as f:
            f.write("# Add imports here")
    
    file_path = os.path.join(path, 'component.py')
    if not os.path.exists(file_path):         
        with open(file_path, 'w') as f:
            f.write("# Define your report component in this package")
            
        
    