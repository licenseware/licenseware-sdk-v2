"""

Here all cli functions are gathered and decorated with typer app decorator.

"""
import json
import os
import shutil
import time
from urllib.parse import urljoin

import requests
import typer

from licenseware.cli.app_pkg_creator import AppPackageCreator
from licenseware.cli.app_root_files_creator import AppRootFilesCreator
from licenseware.cli.devops_creator import DevOpsCreator
from licenseware.cli.report_component_creator import ReportComponentCreator
from licenseware.cli.report_creator import ReportCreator
from licenseware.cli.restx_controller_creator import RestxControllerCreator
from licenseware.cli.test_creator import TestCreator
from licenseware.cli.unittest_file_creator import UnittestFileCreator
from licenseware.cli.uploader_creator import UploaderCreator
from licenseware.cli.utils import get_env_value, get_random_int

app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic files/folders/code creation
    """,
)


@app.command()
def new_app(app_id: str):
    """
    Create the base package for a service
    """

    AppPackageCreator.create()
    DevOpsCreator(app_id).create()
    AppRootFilesCreator(app_id).create()

    typer.echo("App files/folders created")


@app.command()
def new_controller(controller_name: str):
    """
    Given controller_name create a new flask restx controller
    Imports and registration will be handled automatically
    """

    RestxControllerCreator(controller_name).create()
    typer.echo(f"RestX Controller `{controller_name}` created")


@app.command()
def new_unittest(test_name: str):
    """
    Given test_name create a new unittest for pytest
    It will create also a folder for test files
    """

    UnittestFileCreator(test_name).create()
    typer.echo(f"Unittest `{test_name}` created")


@app.command()
def new_uploader(uploader_id: str):
    """
    Given uploader_id build a new uploader

    The package structure for the uploader will be created, imports and registration will be handled also.
    """

    UploaderCreator(uploader_id).create()
    typer.echo(f"Uploader `{uploader_id}` created")


@app.command()
def new_report(report_id: str):
    """
    Given report_id build a new report

    The package structure for the report will be created, imports and registration will be handled also.
    """

    ReportCreator(report_id).create()
    typer.echo(f"Report `{report_id}` created")


@app.command()
def new_report_component(component_id: str, component_type: str):
    """
    Given component_id and component_type build a new report component

    Some component types are:
    - summary
    - pie
    - bar_vertical
    - table

    The package structure for the report component will be created, imports and registration will be handled manually.

    """

    ReportComponentCreator(component_id, component_type).create()
    typer.echo(f"Report component `{component_id}` of type `{component_type}` created")


@app.command()
def recreate_files():
    """Recreate files that are needed but missing"""

    app_id = get_env_value("APP_ID")
    AppPackageCreator.create()
    DevOpsCreator(app_id).create()
    AppRootFilesCreator(app_id).create()
    typer.echo("Inexisting files were recreated")


@app.command()
def build_docs():
    """
    Build app html docs
    """

    os.system("pdoc --html --output-dir app-docs app")

    timeout = 10
    count = 0
    while not os.path.exists("app-docs/app"):
        time.sleep(1)
        count += 1
        if count >= timeout:
            raise Exception("Make sure pdoc is installed and app package is available")

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    shutil.move("app-docs/app", "docs")
    shutil.rmtree("app-docs")


@app.command()
def build_sdk_docs():
    """
    Build licenseware sdk html docs
    """

    os.system("pdoc --html --output-dir sdk-docs licenseware")

    timeout = 10
    count = 0
    while not os.path.exists("sdk-docs/licenseware"):
        time.sleep(1)
        count += 1
        if count >= timeout:
            raise Exception(
                "Make sure pdoc is installed and licenseware package is available"
            )

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    shutil.move("sdk-docs/licenseware", "docs")
    shutil.rmtree("sdk-docs")


@app.command()
def create_tests(test_email: str = None, swagger_url: str = None):
    """
    Create tests from swagger docs

    Command example:

    >> licenseware create-tests --test-email=alin+test@licenseware.io --swagger-url=http://localhost:5000/integration/swagger.json

    Or

    >> licenseware create-tests

    On the second command defaults will we used

    """

    if swagger_url is None:
        base_url = get_env_value("APP_HOST")
        swagger_url = base_url + "/" + get_env_value("APP_ID") + "/swagger.json"

    if test_email is None:
        test_email = f"alin+{get_random_int()}@licenseware.io"

    typer.echo(f"Generating tests for '{test_email}' from '{swagger_url}'")

    ignoretests = None
    if os.path.exists(".ignoretests"):
        typer.echo(
            "Found `.ignoretests` file will ignore test creation for specified files"
        )
        with open(".ignoretests") as f:
            ignoretests = f.readlines()
        ignoretests = [
            f.strip()
            for f in ignoretests
            if (f.startswith("test_") or f.startswith("_test_"))
            and f.strip().endswith(".py")
        ]
        typer.echo(ignoretests)
    else:
        typer.echo("Didn't found `.ignoretests` will create tests for all endpoints")

    tg = TestCreator(swagger=swagger_url, email=test_email, ignore_files=ignoretests)

    tg.generate_tests()

    typer.echo("Tests generated! Checkout `tests` folder!")


auth = typer.Typer(name="auth")


@auth.command()
def login(email: str, password: str, server_url: str = "https://api.licenseware.io"):
    url = urljoin(server_url, "/auth/login")
    response = requests.post(url, json={"email": email, "password": password})
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.text}")

    print(json.dumps(response.json()))


app.add_typer(auth)
