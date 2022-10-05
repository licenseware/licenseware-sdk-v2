from .report_component_types import RCTypes


class DataNarrativeAttrs:
    """
    Usage:
    ```py

    dn = (
        DataNarrativeAttrs()
        .attr(value_key="data")
    )

    ```
    Data Narrative SAMPLE

    {
        'series': {
            'value_key': 'data'
        }
    }

    """

    def __init__(self):
        self.component_type = RCTypes.DATA_NARRATIVE
        self.metadata = {"series": {}}

    def attr(self, *, value_key: str):

        if len(self.metadata["series"]) > 0:
            raise AttributeError("Only one `value_key` can be set")  # pragma no cover

        self.metadata["series"].update({"value_key": value_key})

        return self
