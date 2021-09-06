import os
from .app_dirs import app_path, create_app_dirs


def create_report(name:str):
    
    if not os.path.exists(os.path.join(app_path, 'reports')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'reports', name)
    if not os.path.exists(path): os.makedirs(path)
         
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write("# Add imports here")
        
    with open(os.path.join(path, 'report.py'), 'w') as f:
        f.write("# Define your report in this package")
        