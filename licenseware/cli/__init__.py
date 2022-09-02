"""
This module provides useful CLI commands for automatic creation of files/folders/packages.

Use `licenseware --help` for viewing available commands

```bash
Usage: licenseware [OPTIONS] COMMAND [ARGS]...

  Useful CLI commands for automatic files/folders/code creation

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  build-docs            Build app html docs
  build-sdk-docs        Build licenseware sdk html docs
  create-tests          Create tests from swagger docs Command example: >>...
  new-app               Create the base package for a service
  new-report            Given report_id build a new report The package...
  new-report-component  Given component_id and component_type build a new...
  new-uploader          Given uploader_id build a new uploader The package...
  recreate-files        Recreate files that are needed but missing
```

The most common commands are:


# Create a new app

- Create a new github repository with the name of your service (ex: your-service)
- Clone it
- Inside the cloned repo run `licenseware new-app your-service` (this will create the boilerplate files for a new app)


# Create a new uploader

Inside the cloned repo run:
- `licenseware new-uploader uploader_name` (this will create the boilerplate files for a new uploader)


# Create a new report

Inside the cloned repo run:
- `licenseware new-report report_name` (this will create the boilerplate files for a new report)

In the report you will import the report components created with the following command:
- `licenseware new-report-component component_name component_type`

The available component types are:
- summary
- pie
- bar_vertical
- table

More component types can be added in `licenseware/report_components/attributes`.


# Create boilerplate tests

Bellow command will use the swagger docs for generating a test case for each endpoint.
What remains on the developer side is to provide seed data (if needed) and to do a cleanup after the test run.

Inside the cloned repo run:
- `licenseware create-tests` (this will create the boilerplate tests that can run with `tox tests/test_*`)


# Recreate outdated files 

Let's say some updates were made on the SDK devops files (github workflows, aws cloudformation templates etc), 
instead of modifing manually the files to match the new SDK format you can delete the files that needs to be updated 
and run:  

- `licenseware recreate-files` (which is the same as `licenseware new-app app_name`, but the app_name will be taken from envs)



"""

from .cli import app


def cli_entrypoint():
    # This function needs to be referenced in the setup.py file
    app()
