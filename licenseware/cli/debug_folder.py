import os
from licenseware.utils.logger import log

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template

debug_path = './debug'
debug_jupyter_path = './debug/jupyter'


resources_filenames = {
    'jupyter-docker-compose.yml': 'jupyter-docker-compose.yml',
    'jupyter-requirements.txt': 'jupyter-requirements.txt',
    'debug-env.app_id': '.env.{app_id}',
    'debug-env.debug': '.env.debug',
}


def create_debug_folder(app_id: str = None):

    if not os.path.exists(debug_jupyter_path):
        os.makedirs(debug_jupyter_path)

    app_id_trimed = app_id.split('-')[0].lower()

    for rname, fname in resources_filenames.items():

        if rname.startswith("debug"):
            fpath = os.path.join(debug_path, fname.format(app_id=app_id_trimed))
            if os.path.exists(fpath): continue
        elif rname.startswith("jupyter"):
            fpath = os.path.join(debug_path, fname.format(app_id=app_id_trimed))
            if os.path.exists(fpath): continue

        raw_contents = pkg_resources.read_text(resources, rname)
        tmp = Template(raw_contents)
        file_contents = tmp.render(app_id=app_id_trimed)
        with open(fpath, 'w') as f:
            f.write(file_contents)
