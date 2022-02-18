import os
from .app_dirs import app_path, create_app_dirs

from licenseware import resources
import importlib.resources as pkg_resources

from jinja2 import Template


def _create_report_init_file(path: str, report_id: str):
    file_path = os.path.join(path, '__init__.py')
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_report__init__.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(report_id=report_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _create_report_file(path: str, report_id: str):
    file_path = os.path.join(path, f'{report_id}.py')
    if not os.path.exists(file_path):
        raw_contents = pkg_resources.read_text(resources, '_report.py')
        tmp = Template(raw_contents)
        file_contents = tmp.render(report_id=report_id)

        with open(file_path, 'w') as f:
            f.write(file_contents)


def _add_report_import_to_app_init_file(report_id: str):
    import_report_str = f'from app.reports.{report_id} import {report_id}_report'
    register_report_str = f'App.register_report({report_id}_report)'

    app_init_path = os.path.join(app_path, '__init__.py')

    with open(app_init_path, 'r') as f:
        data = f.readlines()

    # Importing report 
    data.insert(data.index('from licenseware.app_builder import AppBuilder\n') + 1, import_report_str)
    data.insert(data.index('from licenseware.app_builder import AppBuilder\n') + 2, '\n')

    # Registering report
    data.insert(data.index(')\n') + 1, register_report_str)
    data.insert(data.index(')\n') + 2, '\n')

    data = "".join(data)

    with open(app_init_path, 'w') as f:
        f.write(data)


def create_report(report_id: str):
    if not os.path.exists(os.path.join(app_path, 'reports')):
        create_app_dirs()

    path = os.path.join(app_path, 'reports', report_id)
    if not os.path.exists(path): os.makedirs(path)

    _create_report_init_file(path, report_id)
    _create_report_file(path, report_id)
    _add_report_import_to_app_init_file(report_id)
