from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class DetailedSummaryAttrs:
    """
    Usage:

    ```py

    detailed_summary = (
        DetailedSummaryAttrs()
        .attr_header(
            label_key="operating_system",
            value_key="number_of_devices",
            icon=Icons.SERVERS
        )
        .attr_detail(
            label_key="devices_by_type.device_type",
            label_description="Device Type",
            value_key="devices_by_type.number_of_devices",
            value_description="Number of Devices"
        )
    )

    ```

    Detailed Summary SAMPLE

    {
        "header_columns": [
            {
                "label_key": "operating_system",
                "label_description": "Operating System",
                "icon": "ServersIcon",
            },
            {
                "value_key": "number_of_devices",
                "value_description": "Number of Devices",
            },
        ],
        "detail_columns": [
            {
                "label_key": "devices_by_type.device_type",
                "label_description": "Device Type",
            },
            {
                "value_key": "devices_by_type.number_of_devices",
                "value_description": "Number of Devices",
            },
        ],
    }

    SAMPLE DATA:

    [
        {
            "operating_system": "Other",
            "number_of_devices": 2,
            "devices_by_type": [
                {
                    "operating_system": "Other",
                    "device_type": "Virtual",
                    "number_of_devices": 2
                }
            ]
        },
        {
            "operating_system": "ESX",
            "number_of_devices": 48,
            "devices_by_type": [ # in frontend will make a sum of `number_of_devices`
                {
                    "operating_system": "ESX",
                    "device_type": "Cluster",
                    "number_of_devices": 5
                },
                {
                    "operating_system": "ESX",
                    "device_type": "Physical",
                    "number_of_devices": 43
                }
            ]
        }
    ]

    """

    def __init__(self):
        self.component_type = RCTypes.DETAILED_SUMMARY
        self._metadata = {"header_columns": [], "detail_columns": []}

    @property
    def metadata(self):
        assert len(self._metadata["header_columns"]) > 0
        assert len(self._metadata["detail_columns"]) > 0
        return self._metadata

    def attr_header(
        self,
        *,
        label_key: str,
        value_key: str,
        label_description: str = None,
        value_description: str = None,
        icon: str = None
    ):

        if label_description is None:
            altstr = get_altered_strings(label_key)
            label_description = altstr.title

        if value_description is None:
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self._metadata["header_columns"].extend(
            [
                {
                    "label_key": label_key,
                    "label_description": label_description,
                    "icon": icon,
                },
                {
                    "value_key": value_key,
                    "value_description": value_description,
                },
            ]
        )

        return self

    def attr_detail(
        self,
        *,
        label_key: str,
        value_key: str,
        label_description: str = None,
        value_description: str = None,
        icon: str = None
    ):

        if label_description is None:  # pragma no cover
            altstr = get_altered_strings(label_key)
            label_description = altstr.title

        if value_description is None:  # pragma no cover
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self._metadata["detail_columns"].extend(
            [
                {
                    "label_key": label_key,
                    "label_description": label_description,
                    "icon": icon,
                },
                {
                    "value_key": value_key,
                    "value_description": value_description,
                },
            ]
        )

        return self
