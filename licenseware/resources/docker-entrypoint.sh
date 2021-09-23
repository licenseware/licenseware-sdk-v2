#!/bin/bash
set -e

# Making sure aws updates requirements
pip uninstall -y licenseware && pip install -r requirements.txt 

honcho start
