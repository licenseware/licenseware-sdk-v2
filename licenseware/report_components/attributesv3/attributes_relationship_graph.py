from licenseware.utils.alter_string import get_altered_strings

from .report_component_types import RCTypes


class RelationshipGraphAttrs:
    """
    Usage:
    ```py

    relationship_graph = (
        RelationshipGraphAttrs()
        .attr_series(label_key="device_name")
        .attr_series(label_key="device_type")
        .attr_categories(category_key="virtualization_type")
    )

    ```

    Relationship Graph SAMPLE

    {
        'series':
        [
            {
                'label_key': 'device_name',
                'label_description': 'Device Name',
            },
            {
                'label_key': 'device_type',
                'label_description': 'Device Type',
            },

        ],
        'categories': [
            {
                'category_key': 'virtualization_type',
                'category_label': 'Virtualization Type',
            }
        ]
    }

    """

    def __init__(self):
        self.component_type = RCTypes.RELATIONSHIP_GRAPH
        self._metadata = {"series": [], "categories": []}

    @property
    def metadata(self):
        assert len(self._metadata["series"]) > 0
        assert len(self._metadata["categories"]) > 0
        return self._metadata

    def attr_series(self, *, label_key: str, label_description: str = None):

        if label_description is None:
            altstr = get_altered_strings(label_key)
            label_description = altstr.title

        self._metadata["series"].append(
            {
                "label_key": label_key,
                "label_description": label_description,
            }
        )

        return self

    def attr_categories(self, *, category_key: str, category_label: str = None):

        if category_label is None:
            altstr = get_altered_strings(category_key)
            category_label = altstr.title

        self._metadata["categories"].append(
            {
                "category_key": category_key,
                "category_label": category_label,
            }
        )

        return self
