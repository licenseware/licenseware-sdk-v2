"""

Here all cli functions are gathered and decorated with typer app decorator.

"""
import os
import random
import time
import shutil
import typer
from .app_pkg_creator import AppPackageCreator
from .devops_creator import DevOpsCreator
from .app_root_files_creator import AppRootFilesCreator
from .uploader_creator import UploaderCreator
# from .report import create_report
# from .uploader import create_uploader
# from .report_component import create_report_component
# from .env_data import get_env_value
# from licenseware.test_generator import TestGenerator



app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic files/folders/code creation
    """
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
def new_uploader(uploader_id: str):
    """ 
        Given uploader_id build a new uploader 
        
        The package structure for the uploader will be created, imports and registration will be handled also.
    """
    
    UploaderCreator(uploader_id).create()
    typer.echo(f"Uploader `{uploader_id}` created")
    
    
# @app.command()
# def new_report(report_id: str):
#     """ 
#         Given report_id build a new report 
        
#         The package structure for the report will be created, imports and registration will be handled also.
#     """
#     create_report(report_id)
#     # typer.echo("Report structure created")
    
    
# @app.command()
# def new_report_component(component_id: str, component_type: str):
#     """
#         Given component_id and component_type build a new report component 

#         Some component types are:
#         - summary
#         - pie
#         - bar_vertical
#         - table
    
    
#         The package structure for the report component will be created, imports and registration will be handled manually.
        
#     """
#     create_report_component(component_id, component_type)
#     # typer.echo("Report component structure created")
    
    


# @app.command()
# def build_docs():
#     """
#         Build app html docs
#     """
    
#     os.system("pdoc --html --output-dir app-docs app")
    
#     timeout = 10
#     count = 0
#     while not os.path.exists("app-docs/app"):
#         time.sleep(1)
#         count += 1
#         if count >= timeout:
#             raise Exception("Make sure pdoc is installed and app package is available")
            
#     if os.path.exists("docs"): shutil.rmtree("docs")
#     shutil.move("app-docs/app", "docs")
#     shutil.rmtree("app-docs")


    

# @app.command()
# def build_sdk_docs():
#     """
#         Build licenseware sdk html docs
#     """
    
#     os.system("pdoc --html --output-dir sdk-docs licenseware")
    
#     timeout = 10
#     count = 0
#     while not os.path.exists("sdk-docs/licenseware"):
#         time.sleep(1)
#         count += 1
#         if count >= timeout:
#             raise Exception("Make sure pdoc is installed and licenseware package is available")
            
#     if os.path.exists("docs"): shutil.rmtree("docs")
#     shutil.move("sdk-docs/licenseware", "docs")
#     shutil.rmtree("sdk-docs")



# @app.command()
# def recreate_files():
#     """ Recreate files that are needed but missing  """

#     create_app_dirs(get_env_value("APP_ID"))



# @app.command()
# def create_tests(test_email: str = None, swagger_url: str = None):
#     """ 
#         Create tests from swagger docs

#         Command example:
        
#         >> licenseware create-tests --test-email=alin+test@licenseware.io --swagger-url=http://localhost:5000/integration/swagger.json
        
#         Or

#         >> licenseware create-tests

#         On the second command defaults will we used

#     """

#     if swagger_url is None:
#         base_url = get_env_value("APP_HOST")
#         swagger_url = base_url + '/' + get_env_value("APP_ID").replace("-service", "") + "/swagger.json"

#     if test_email is None:
#         test_email = f"alin+{random.randint(1000, 9999)}@licenseware.io"

#     typer.echo(f"Generating tests for '{test_email}' from '{swagger_url}'")

#     tg = TestGenerator(swagger=swagger_url, email=test_email)

#     tg.generate_tests()

#     typer.echo("Tests generated! Checkout `tests` folder!")