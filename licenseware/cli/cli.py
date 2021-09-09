"""

Here all cli functions are gathered and decorated with typer app decorator.

"""
import os
import time
import shutil
import typer
from .app_dirs import create_app_dirs
from .report import create_report
from .uploader import create_uploader
from .report_component import create_report_component



app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic code generation, files and folders creation.
    """
)


@app.command()
def new_app(app_id:str):
    """ 
        Given app_id make a new app
        
        The package structure for the app will be created and the app_id will be added to .env file
         
    """
    create_app_dirs(app_id)
    # typer.echo("App structure created")
    
        
@app.command()
def new_uploader(uploader_id: str):
    """ 
        Given uploader_id make a new uploader 
        
        The package structure for the uploader will be created, imports and registration will be handled also.
    """
    create_uploader(uploader_id)
    # typer.echo("Uploader structure created")
    
    
@app.command()
def new_report(report_id: str):
    """ 
        Given report_id make a new report 
        
        The package structure for the report will be created, imports and registration will be handled also.
    """
    create_report(report_id)
    # typer.echo("Report structure created")
    
    
@app.command()
def new_report_component(component_id: str, component_type: str = None):
    """
        Given component_id make a new report component 
        
        Argument component_type will be taken if not provided from component_id (ex: virtualization_summary -> summary will be the component_type)
        
        The package structure for the report component will be created, imports and registration will be handled also.
        
    """
    create_report_component(component_id, component_type)
    # typer.echo("Report component structure created")
    
    


@app.command()
def make_docs():
    """
        Make app html docs
    """
    
    os.system("pdoc --html --output-dir app-docs app")
    
    timeout = 10
    count = 0
    while not os.path.exists("app-docs/app"):
        time.sleep(1)
        count += 1
        if count >= timeout:
            raise Exception("Make sure pdoc is installed and app package is available")
            
    if os.path.exists("docs"): shutil.rmtree("docs")
    shutil.move("app-docs/app", "docs")
    shutil.rmtree("app-docs")


    

@app.command()
def make_sdk_docs():
    """
        Make licenseware sdk html docs
    """
    
    os.system("pdoc --html --output-dir sdk-docs licenseware")
    
    timeout = 10
    count = 0
    while not os.path.exists("sdk-docs/licenseware"):
        time.sleep(1)
        count += 1
        if count >= timeout:
            raise Exception("Make sure pdoc is installed and licenseware package is available")
            
    if os.path.exists("docs"): shutil.rmtree("docs")
    shutil.move("sdk-docs/licenseware", "docs")
    shutil.rmtree("sdk-docs")

    