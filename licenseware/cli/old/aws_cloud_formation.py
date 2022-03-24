import os
from licenseware.utils.logger import log

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template

cloudformation_path = './cloudformation-templates'

resources_filenames = {
    'cloud-formation-app_id-api_prod.yml': '{app_id}-api_prod.yml',
    'cloud-formation-app_id-api.yml': '{app_id}-api.yml'
}


def create_aws_cloud_formation(app_id: str = None):
    if not os.path.exists(cloudformation_path):
        os.makedirs(cloudformation_path)

    app_id_trimed = app_id.split('-')[0].lower()

    for rname, fname in resources_filenames.items():

        fpath = os.path.join(cloudformation_path, fname.format(app_id=app_id_trimed))
        if os.path.exists(fpath): continue

        raw_contents = pkg_resources.read_text(resources, rname)
        tmp = Template(raw_contents)
        file_contents = tmp.render(app_id=app_id_trimed)
        with open(fpath, 'w') as f:
            f.write(file_contents)
