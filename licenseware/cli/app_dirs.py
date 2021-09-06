import os


app_path = './app'
app_dirs = [
    'common',
    'reports',
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
        with open(os.path.join(path, '__init__.py'), 'w') as f:
            f.write("# Add imports here")
            
    with open(os.path.join(app_path, '__init__.py'), 'w') as f:
        f.write("# Add imports here")

    # TODO move it to resources package instead of doc strings
    with open('main.py', 'w') as f:
        f.write("#TODO")
