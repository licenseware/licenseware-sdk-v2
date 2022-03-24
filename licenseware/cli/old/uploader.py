import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template


def _create_uploader_init_file(path: str, uploader_id: str):
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_uploader__init___.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _create_uploader_worker_file(path: str, uploader_id: str):
    file_path = os.path.join(path, 'worker.py')
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_uploader_worker.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _create_uploader_validator_file(path: str, uploader_id: str):
    file_path = os.path.join(path, 'validator.py')
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_uploader_validator.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _add_uploader_import_to_app_init_file(uploader_id: str):
    import_uploader_str = f'from app.uploaders.{uploader_id} import {uploader_id}_uploader'
    register_uploader_str = f'App.register_uploader({uploader_id}_uploader)'

    app_init_path = os.path.join(app_path, '__init__.py')

    with open(app_init_path, 'r') as f:
        data = f.readlines()

    # Importing uploader 
    data.insert(data.index('from licenseware.app_builder import AppBuilder\n') + 1, import_uploader_str)
    data.insert(data.index('from licenseware.app_builder import AppBuilder\n') + 2, '\n')

    # Registering uploader
    data.insert(data.index(')\n') + 1, register_uploader_str)
    data.insert(data.index(')\n') + 2, '\n')

    data = "".join(data)

    with open(app_init_path, 'w') as f:
        f.write(data)


def _create_test_filename_validation(uploader_id: str):
    fname = f'test_filename_validation_{uploader_id}.py'
    file_path = os.path.join('tests', fname)
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_test_filename_validation_uploader_id.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _create_test_filecontent_validation(uploader_id: str):
    fname = f'test_filecontent_validation_{uploader_id}.py'
    file_path = os.path.join('tests', fname)
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_test_filecontent_validation_uploader_id.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(uploader_id=uploader_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _create_test_files_folder(uploader_id: str):
    test_files_path = f"./test_files/{uploader_id}"
    if not os.path.exists(test_files_path):
        os.makedirs(test_files_path)


def create_uploader(uploader_id: str):
    if not os.path.exists(os.path.join(app_path, 'uploaders')):
        create_app_dirs()

    path = os.path.join(app_path, 'uploaders', uploader_id)
    if not os.path.exists(path): os.makedirs(path)

    _create_uploader_init_file(path, uploader_id)
    _create_uploader_worker_file(path, uploader_id)
    _create_uploader_validator_file(path, uploader_id)
    _add_uploader_import_to_app_init_file(uploader_id)
    _create_test_filename_validation(uploader_id)
    _create_test_filecontent_validation(uploader_id)
    _create_test_files_folder(uploader_id)
