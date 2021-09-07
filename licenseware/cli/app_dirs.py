import os
from licenseware.utils.logger import log


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


def create_app_dirs():
    
    created_paths = []
    for dir_name in app_dirs:
        path = os.path.join(app_path, dir_name)
        if not os.path.exists(path): os.makedirs(path)
        created_paths.append(path)
        
    for path in created_paths:
        file_path = os.path.join(path, '__init__.py')         
        if os.path.exists(file_path):
            log.warning("Skipped creating {} because it already exists")
            continue
        with open(file_path, 'w') as f:
            f.write("# Add imports here")
            
            
    file_path = os.path.join(app_path, '__init__.py')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("# Add imports here")


    if not os.path.exists('main.py'):
        with open('main.py', 'w') as f:
            f.write("#TODO")
