"""

Here all cli functions are gathered and decorated with typer app decorator.

"""

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
def new_app():
    """ Creating boilerplate folders for a new app """
    create_app_dirs()
    typer.echo("App structure created")
    
        
@app.command()
def new_uploader(name: str):
    """ Creating boilerplate folders for a new uploader """
    create_uploader(name)
    typer.echo("Uploader structure created")
    
    
@app.command()
def new_report(name: str):
    """ Creating boilerplate folders for a new report """
    create_report(name)
    typer.echo("Report structure created")
    
    
@app.command()
def new_report_component(name: str):
    """ Creating boilerplate folders for a new report component """
    create_report_component(name)
    typer.echo("Report component structure created")
    
    