import os
import typer
from .app_dirs import create_app_dirs
from .report import create_report
from .uploader import create_uploader


app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic code generation, files and folders creation.
    """
)

@app.command()
def new_app():
    """ Creating boilerplate folders for a new app """
    create_app_dirs()
    
        
@app.command()
def new_uploader(name: str):
    """ Creating boilerplate folders for a new uploader """
    create_uploader(name)
    

@app.command()
def new_report(name: str):
    """ Creating boilerplate folders for a new report """
    create_report(name)
    
    