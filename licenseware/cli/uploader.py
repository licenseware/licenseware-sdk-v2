import os
from .app_dirs import app_path, create_app_dirs


def create_uploader(name):
    
    if not os.path.exists(os.path.join(app_path, 'uploaders')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'uploaders', name)
    if not os.path.exists(path): os.makedirs(path)
         
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("# Add imports here")
            
    file_path = os.path.join(path, 'worker.py')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("# Define your worker in this package")
        