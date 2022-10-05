from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class BarHorizontalAttrs:
    """
    Usage:
    ```py

    bar_horizontal = (
        BarHorizontalAttrs()
        .attr(
            xaxis_key="product_name",
            yaxis_key="oracle_processors_required"
        )
    )

    ```
    Bar Horizontal SAMPLE

    {
        "series": [
            {
                "xaxis_key": "product_name"
                "xaxis_description": "Product Name",
            },
            {
                "yaxis_key": "oracle_processors_required",
                "yaxis_description": "Processor Licenses Required",
            },
        ]
    }

    """

    def __init__(self):
        self.component_type = RCTypes.BAR_HORIZONTAL
        self.metadata = {"series": []}

    def attr(
        self,
        *,
        xaxis_key: str,
        yaxis_key: str,
        xaxis_description: str = None,
        yaxis_description: str = None
    ):

        if xaxis_description is None:
            altstr = get_altered_strings(xaxis_key)
            xaxis_description = altstr.title

        if yaxis_description is None:
            altstr = get_altered_strings(yaxis_key)
            yaxis_description = altstr.title

        self.metadata["series"].extend(
            [
                {
                    "xaxis_key": xaxis_key,
                    "xaxis_description": xaxis_description,
                },
                {
                    "yaxis_key": yaxis_key,
                    "yaxis_description": yaxis_description,
                },
            ]
        )

        return self
