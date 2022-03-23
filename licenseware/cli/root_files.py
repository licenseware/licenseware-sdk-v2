import os

from licenseware.utils.logger import log
from licenseware.utils.miscellaneous import generate_id

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template

from .github_workflows import create_github_workflows
from .aws_cloud_formation import create_aws_cloud_formation
from .deploy_folder import create_deploy_folder

# Underscore tells pyoc3 to ignore them from creating docs 
# (otherwise an error will occur)  
resources_filenames = {
    # '_main_example.py': 'main_example.py',
    '_main.py': 'main.py',
    # '_mock_server.py': 'mock_server.py',
    '_setup.py': 'setup.py',
    # 'docker_compose_mongo_redis.yml': 'docker-compose.yml',
    'envlocal': '.envlocal',
    'gitignore': '.gitignore',
    'makefile': 'makefile',
    'README.md': 'README.md',
    'requirements.txt': 'requirements.txt',
    'requirements-dev.txt': 'requirements-dev.txt',
    'requirements-tests.txt': 'requirements-tests.txt',
    # DevOps
    'dockerignore': '.dockerignore',
    'CHANGELOG.md': 'CHANGELOG.md',
    'docker-entrypoint.sh': 'docker-entrypoint.sh',
    'Dockerfile': 'Dockerfile',
    'Dockerfile.stack': 'Dockerfile.stack',
    'Procfile': 'Procfile',
    'Procfile.stack': 'Procfile.stack',
    'version.txt': 'version.txt',
    'tox.ini': 'tox.ini',
    'pre-commit-config.yaml': '.pre-commit-config.yaml',
    'docker-compose.yml': 'docker-compose.yml'
}


def create_test_environment():
    if not os.path.exists("test_files"): os.makedirs("test_files")
    if not os.path.exists("tests"): os.makedirs("tests")

    init_test_file = os.path.join('tests', '__init__.py')
    if not os.path.exists(init_test_file):
        with open(init_test_file, 'w') as f:
            f.write("# Add imports here")

    starter_test_file = os.path.join('tests', 'test_starter.py')
    if not os.path.exists(starter_test_file):
        raw_contents = pkg_resources.read_text(resources, '_test_starter.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render()
        with open(starter_test_file, 'w') as f:
            f.write(file_contents)


def create_root_files(app_id: str):

    for rname, fname in resources_filenames.items():
        if not os.path.exists(fname):
            raw_contents = pkg_resources.read_text(resources, rname)
            tmp = Template(raw_contents)

            file_contents = tmp.render(app_id=app_id)

            with open(fname, 'w') as f:
                f.write(file_contents)

    create_github_workflows(app_id)
    create_aws_cloud_formation(app_id)
    create_deploy_folder(app_id)
    create_test_environment()
