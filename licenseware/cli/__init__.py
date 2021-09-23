# TODO this package could be cleaner

from .cli import app


def cli_entrypoint():
    #This function needs to be referenced in the setup.py file
    app()
    