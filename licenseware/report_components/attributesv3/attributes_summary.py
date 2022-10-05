from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class SummaryAttrs:
    """
    Usage:

    ```py

    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details",
            value_description="Missing parent details",
            icon=Icons.FEATURES
        )
        .attr(value_key="unknown_types")
    )

    ```

    Summary SAMPLE

    {
        "series": [
            {
                "value_key": "missing_parent_details",
                "value_description": "Missing parent details",
                "icon": "FeaturesIcon",
            },
            {
                "value_key": "unknown_types",
                "value_description": "Unknown device types",
                "icon": "ServersIcon",
            },
            {
                "value_key": "missing_cores_info",
                "value_description": "Missing cores info",
                "icon": "CpuIcon",
            },
        ]
    }

    """

    def __init__(self):
        self.component_type = RCTypes.SUMMARY
        self.metadata = {"series": []}

    def attr(self, *, value_key: str, value_description: str = None, icon: str = None):

        if value_description is None:
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self.metadata["series"].append(
            {
                "value_key": value_key,
                "value_description": value_description,
                "icon": icon,
            }
        )

        return self
