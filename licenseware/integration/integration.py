"""

The function `make_integration` is useful for creating integration details which will be validated.

Usage:

```py

from licenseware.integration import make_integration


servicenow_integration = make_integration(
        integration_id="servicenow",
        imported_data=["devices"],
        exported_data=["reports"],
        triggers=["scan"],
        app_id=envs.APP_ID,
        name="Integration Service",
        description="Integrate external services into licenseware ecosystem"
    )


App = AppBuilder(
    name="Integration Service",
    description="Integrate external services into licenseware ecosystem",
    flags=[flags.BETA],
    integration_details=[servicenow_integration]
)

```

"""


from typing import List
from licenseware.common.validators import validate_integration_details

def make_integration(
    integration_id: str, 
    imported_data: List[str],
    exported_data: List[str],
    triggers: List[str],
    app_id:str,
    name:str,
    description:str
):
    """
    Return a dict with the data needed for integration-service 
    Ex:
        {
            'app_id': "odb-service",
            'name': "Oracle Database",
            'description': "Analyse oracle database",
            'integration_id': 'servicenow',
            'imported_data': ["oracle_databases"],
            'exported_data': ["reports"],
            'triggers': ["database_created", "database_deleted", "network_scan"]
        }
    """

    integration_details = {
        'app_id': app_id,
        'name': name,
        'description': description,
        'integration_id': integration_id,
        'imported_data': imported_data,
        'exported_data': exported_data,
        'triggers': triggers
    }

    validate_integration_details(integration_details)

    return integration_details


