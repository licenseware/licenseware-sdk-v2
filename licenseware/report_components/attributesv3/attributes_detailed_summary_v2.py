from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class DetailedSummaryV2Attrs:
    """
    Usage:

    ```py

    detailed_summary = (
        DetailedSummaryV2Attrs()
        .attr(value_key="product_name")
        .attr(value_key="proc_license_cost", value_description="Cost")
        etc
    )

    ```

    Detailed Summary SAMPLE

    {
        "series": [
            {
                "value_description": "Product Name",
                "value_key": "product_name"
            },
            {
                "value_description": "Licensing by CPU",
                "value_key": "oracle_processors_required",
            },
            {
                "value_description": "Cost",
                "value_key": "proc_license_cost",
                "type": "currency",
                "currency": "USD",
            },
            {
                "value_description": "Licensing by NUP minimum",
                "value_key": "nup_minimum",
            },
            {
                "value_description": "Cost",
                "value_key": "nup_license_cost",
                "type": "currency",
                "currency": "USD",
            },
        ]
    }

    SAMPLE DATA:



    """

    def __init__(self):
        self.component_type = RCTypes.DETAILED_SUMMARY_V2
        self.metadata = {"series": []}

    def attr(
        self,
        *,
        value_key: str,
        value_description: str = None,
        type: str = None,
        currency: str = None
    ):

        if value_description is None:
            altstr = get_altered_strings(value_key)
            value_description = altstr.title

        self.metadata["series"].append(
            {
                "value_key": value_key,
                "value_description": value_description,
                "type": type,
                "currency": currency,
            }
        )

        return self
