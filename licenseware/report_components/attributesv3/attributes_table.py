from licenseware.utils.alter_string import get_altered_strings

from .column_types import ColumnTypes
from .report_component_types import RCTypes


class TableAttrs:
    """
    Usage:

    ```py

    table = (
        TableAttrs()
        .attr(prop= "device_name")
        .attr( prop= "number_of_devices", name="Device Numbers", type=ColumnTypes.STRING)
        etc
    )

    ```

    Table SAMPLE

    {
        "columns": [
            {
                "name": "Device Name",
                "prop": "device_name",
                "type": "string"
            },
            {
                "name": "Product Category",
                "prop": "product_category",
                "type": "string",
            },
        ]
    }
    """

    def __init__(self):
        self.component_type = RCTypes.TABLE
        self.metadata = {"columns": []}

    def attr(self, prop: str, *, name: str = None, type: str = ColumnTypes.STRING):

        if name is None:
            altstr = get_altered_strings(prop)
            name = altstr.title

        self.metadata["columns"].append(
            {
                "name": name,
                "prop": prop,
                "type": type,
            }
        )

        return self
