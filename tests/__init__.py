"""
This is here to load environment variables for tests to run.

You can specify test order in the makefile

Make sure to delete __pycache__ folder before each test


rm -rf tests/__pycache__
python3 -m unittest tests/test_sdk_cli.py
rm -rf tests/__pycache__
python3 -m unittest tests/*
rm -rf app


"""

from dotenv import load_dotenv
load_dotenv()  

from licenseware.utils.miscellaneous import generate_id


report_id = "virtualization_details" + generate_id()
component_id = "virtual_overview" + generate_id()
uploader_id = "rv_tools" + generate_id()


tenant_id = '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'
 
headers = {
    'Tenantid': tenant_id,
    'Authorization': 'TheAuthorization' 
}



