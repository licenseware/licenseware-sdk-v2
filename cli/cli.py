import os
import click


'''

.
├── .env
├── main.py
├── mock_server.py
└── app
    ├── common
    │   └── __init__.py
    ├── controllers
    │   └── __init__.py
    ├── __init__.py
    ├── reports
    │   └── __init__.py
    ├── uploaders
    │   └── __init__.py
    └── utils
        └── __init__.py
        
        
'''



@click.command()
@click.option('--create-app', required=False, default='testapp')
def cli(create_app):
    os.mkdir()
    click.echo(f'{create_app} created')
    
    
    
    
if __name__ == '__main__':
    cli()