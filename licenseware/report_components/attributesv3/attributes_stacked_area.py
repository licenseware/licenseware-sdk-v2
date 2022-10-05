from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class StackedAreaAttrs:
    """
    Usage:
    ```py


    ```
    Stacked Area SAMPLE

    {
        "series": {
            "xaxis": [
                {
                    "description": "Option Name",
                    "key": "option_name"
                }
            ],
            "yaxis": [
                {
                    "label_description": "Status",
                    "label_key": "details.result"
                },
                {
                    "value_description": "Number of Databases",
                    "value_key": "details.count"
                },

            ]
        }
    }

    """

    def __init__(self):
        self.component_type = RCTypes.STACKED_AREA
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
