"""

Here all cli functions are gathered and decorated with typer app decorator.

"""
import os
import re
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
        Given app_id build a new app
        
        The package structure for the app will be created and the app_id will be added to .env file
         
    """
    create_app_dirs(app_id)
    # typer.echo("App structure created")
    
        
@app.command()
def new_uploader(uploader_id: str):
    """ 
        Given uploader_id build a new uploader 
        
        The package structure for the uploader will be created, imports and registration will be handled also.
    """
    create_uploader(uploader_id)
    # typer.echo("Uploader structure created")
    
    
@app.command()
def new_report(report_id: str):
    """ 
        Given report_id build a new report 
        
        The package structure for the report will be created, imports and registration will be handled also.
    """
    create_report(report_id)
    # typer.echo("Report structure created")
    
    
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
    create_report_component(component_id, component_type)
    # typer.echo("Report component structure created")
    
    


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
            
    if os.path.exists("docs"): shutil.rmtree("docs")
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
            raise Exception("Make sure pdoc is installed and licenseware package is available")
            
    if os.path.exists("docs"): shutil.rmtree("docs")
    shutil.move("sdk-docs/licenseware", "docs")
    shutil.rmtree("sdk-docs")

    


@app.command()
def start_mock_server():
    """
        Start the mock server needed which is a placeholder for registry-service and auth-service
    """
    os.system("uwsgi --http 0.0.0.0:5000 -w mock_server:app --processes 4")



@app.command()
def start_dev_server():
    """
        Start the development server (flask server with debug on)
    """
    os.system("python3 main.py")



@app.command()
def start_prod_server():
    """
        Start the production server (uwsgi server with 4 processes)
    """
    os.system("uwsgi --http 0.0.0.0:4000 -w main:app --processes 4")

    
    
@app.command()
def start_background_worker():
    """
        Start the redis background worker with 4 processes and with queue of app id from .env
    """
    
    if not os.path.exists('.env'):
        raise Exception("Expected '.env' file to be found in this directory")
        
    with open('.env', 'r') as f:
        env_data = f.read()
        
    app_id = None
    m = re.search(r"APP_ID=(.*)", env_data)
    if m: app_id = m.group(1)

    if app_id:
        os.system(f"flask worker -p4 -Q{app_id}")
    else:#listen to all queues
        os.system(f"flask worker -p4")

    
