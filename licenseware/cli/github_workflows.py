import os
from licenseware.utils.logger import log

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template


git_workflows_path = '.github/workflows'

resources_filenames = {
    'app_id-api_prod.yml': '{app_id}-api_prod.yml',
    'app_id-api.yml': '{app_id}-api.yml',
    'release-please.yml': 'release-please.yml'
}



def create_github_workflows(app_id:str = None):
    
    if not os.path.exists(git_workflows_path): 
        os.makedirs(git_workflows_path)
    
    for rname, fname in resources_filenames.items():  
        fpath = os.path.join(git_workflows_path, fname.format(app_id=app_id))
        if os.path.exists(fpath): continue
        raw_contents = pkg_resources.read_text(resources, rname)
        tmp = Template(raw_contents)
        file_contents = tmp.render(app_id=app_id)
        with open(fpath, 'w') as f:
            f.write(file_contents)
