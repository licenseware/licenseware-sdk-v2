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
    """ Make structure for a new app """
    create_app_dirs()
    # typer.echo("App structure created")
    
        
@app.command()
def new_uploader(uploader_id: str):
    """ Make structure for a new uploader """
    create_uploader(uploader_id)
    # typer.echo("Uploader structure created")
    
    
@app.command()
def new_report(report_id: str):
    """ Make structure for a new report """
    create_report(report_id)
    # typer.echo("Report structure created")
    
    
@app.command()
def new_report_component(component_id: str, component_type: str):
    """ Make structure for a new report component """
    create_report_component(component_id, component_type)
    # typer.echo("Report component structure created")
    
    