from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class StackedBarVerticalAttrs:
    """
    Usage:

    ```py

    stacked_bar_vertical = (
        StackedBarVerticalAttrs()
        .attr_xaxis(key="_id", description="Product Name")
        .attr_yaxis(
            label_key="details.license_metric",
            label_description="License Metric",
            value_key="details.quantity",
            value_description="Quantity"
        )
    )

    ```

    Stacked Bar Vertical SAMPLE

    {
        "series": {
            "xaxis": [
                {
                    "description": "Product Name",
                    "key": "_id"
                }
            ],
            "yaxis": [
                {
                    "label_key": "details.license_metric"
                    "label_description": "License Metric",
                },
                {
                    "value_key": "details.quantity",
                    "value_description": "Quantity",
                },
            ],
        }
    }

    """

    def __init__(self):
        self.component_type = RCTypes.STACKED_BAR_VERTICAL
        self._metadata = {"series": {"xaxis": [], "yaxis": []}}

    @property
    def metadata(self):
        assert len(self._metadata["series"]["xaxis"]) > 0
        assert len(self._metadata["series"]["yaxis"]) > 0
        return self._metadata

    def attr_xaxis(self, *, key: str, description: str):

        self._metadata["series"]["xaxis"].append(
            {
                "key": key,
                "description": description,
            }
        )

        return self

    def attr_yaxis(
        self,
        *,
        label_key: str,
        value_key: str,
        label_description: str = None,
        value_description: str = None
    ):

        if label_description is None:  # pragma no cover
            altstr = get_altered_strings(label_key)
            label_description = altstr.title

        if value_description is None:  # pragma no cover
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self._metadata["series"]["yaxis"].extend(
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
