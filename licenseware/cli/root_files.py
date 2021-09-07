import os

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template

     
def create_root_files(*filenames):
    
    for filename in filenames:
        
        hidden_file = filename in {'env', 'gitignore'}           
        file_path = '.' + filename if hidden_file else filename
        
        if not os.path.exists(file_path):
            raw_contents = pkg_resources.read_text(resources, filename)
            tmp = Template(raw_contents)
            file_contents = tmp.render()
            with open(file_path, 'w') as f:
                f.write(file_contents)
