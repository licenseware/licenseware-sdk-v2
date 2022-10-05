from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class PieAttrs:
    """
    Usage:
    ```py

    pie = (
        PieAttrs()
        .attr(
            label_key="product_name",
            label_description="WebLogic Edition",
            value_key="number_of_devices",
            value_description="Number of Devices",
        )
        .attr(label_key="device_name", value_key="devices_numbers")
    )

    ```
    PIE SAMPLE

    {
        "series": [
            {
                "label_description": "WebLogic Edition",
                "label_key": "product_name"
            },
            {
                "value_description": "Number of Devices",
                "value_key": "number_of_devices",
            },
        ]
    }
    """

    def __init__(self):
        self.component_type = RCTypes.PIE
        self.metadata = {"series": []}

    def attr(
        self,
        *,
        label_key: str,
        value_key: str,
        value_description: str = None,
        label_description: str = None
    ):

        if label_description is None:
            altstr = get_altered_strings(label_key)
            label_description = altstr.title

        if value_description is None:
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self.metadata["series"].extend(
            [
                {
                    "label_key": label_key,
                    "label_description": label_description,
                },
                {
                    "value_key": value_key,
                    "value_description": value_description,
                },
            ]
        )

        return self
