import os
import typer
from .app_dirs import create_app_dirs, app_dirs, app_path


app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic code generation, files and folders creation.
    """
)



@app.command()
def new_app():
    """
        Creating boilerplate folders for a new app
    """
    create_app_dirs()
    
        
@app.command()
def new_uploader(name: str):
    """
        Creating boilerplate folders for a new uploader
    """
    
    if not os.path.exists(os.path.join(app_path, 'uploaders')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'uploaders', name)
    if not os.path.exists(path): os.makedirs(path)
         
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write("# Add imports here")
        
    with open(os.path.join(path, 'worker.py'), 'w') as f:
        f.write("# Define your worker in this package")
        
    

@app.command()
def new_report(name: str):
    """
        Creating boilerplate folders for a new report
    """
    
    if not os.path.exists(os.path.join(app_path, 'reports')): 
        create_app_dirs()
        
    path = os.path.join(app_path, 'reports', name)
    if not os.path.exists(path): os.makedirs(path)
         
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write("# Add imports here")
        
    with open(os.path.join(path, 'report.py'), 'w') as f:
        f.write("# Define your report in this package")
        
    
    