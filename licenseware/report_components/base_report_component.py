from flask import Request

from licenseware.common.constants import envs
from licenseware.registry_service import register_component
from licenseware.report_components.attributes import (
    attributes_bar_vertical,
    attributes_pie,
    attributes_summary,
    attributes_table,
)
from licenseware.report_components.build_match_expression import (
    build_match_expression,
    condition_switcher,
)
from licenseware.utils.miscellaneous import flat_dict

component_attributes_mapper = {
    "bar_vertical": attributes_bar_vertical,
    "pie": attributes_pie,
    "summary": attributes_summary,
    "table": attributes_table,
}


all_allowed_filters = [
    "equals",
    "contains",
    "in_list",
    "greater_than",
    "greater_or_equal_to",
    "less_than",
    "less_or_equal_to",
]


class BaseReportComponent:
    def __init__(
        self,
        title: str,
        component_id: str,
        component_type: str,
        description: str = None,
        filters: list = None,
        path: str = None,
        order: int = None,
        style_attributes: dict = None,
        attributes: dict = None,
        registration_payload: dict = None,
        sheet_title: str = None,
        **options,
    ):

        if envs.DEPLOYMENT_SUFFIX is not None:
            title = title + envs.DEPLOYMENT_SUFFIX
            component_id = component_id + envs.DEPLOYMENT_SUFFIX

        self.title = title
        self.component_id = component_id
        self.component_type = component_type
        self.description = description
        self.filters = filters
        self.path = path or "/" + component_id
        self.component_path = (
            self.path if self.path.startswith("/") else "/" + self.path
        )
        self.public_component_path = self.component_path + "/public"
        self.snapshot_component_path = self.component_path + "/snapshot"
        self.url = envs.REPORT_COMPONENT_URL + self.component_path
        self.public_url = envs.REPORT_COMPONENT_URL + self.public_component_path
        self.snapshot_url = envs.REPORT_COMPONENT_URL + self.snapshot_component_path
        self.order = order
        self.style_attributes = style_attributes
        self.attributes = attributes
        self.registration_payload = registration_payload
        self.app_id = envs.APP_ID
        self.options = options
        self.sheet_title = sheet_title or self.title

    def build_filter(
        self,
        column: str,
        allowed_filters: list,
        visible_name: str,
        column_type: str = "string",
        validate: bool = True,
    ):
        """
        Will return a dictionary similar to the one bellow:

        {
            "column": "version.edition",
            "allowed_filters": [
                "equals", "contains", "in_list"
            ],
            "visible_name": "Product Edition",
            "column_type": "string" or "number" or TODO add more types here
        }

        The dictionary build will be used to filter mongo

        """

        if validate:

            if " " in column:
                raise ValueError(
                    "Parameter `column` can't contain spaces and must be all lowercase like `device_name`"
                )

            for f in allowed_filters:
                if f not in condition_switcher.keys():
                    raise ValueError(f"Filter {f} not in {condition_switcher.keys()}")

        return dict(
            column=column,
            allowed_filters=allowed_filters,
            visible_name=visible_name,
            column_type=column_type,
        )

    def build_filters_from_columns_attributes(self, attributes: dict):
        """

        Given a dict with 'columns' list attributes similar to the one bellow:

        attributes = {
                "columns": [
                    {
                        "name": "Device Name",
                        "prop": "device_name",
                        "type": "string"
                    },
                    etc
                }]

        Generate a list of column filters like bellow:

        [
            {
                'column': 'device_name',
                'allowed_filters': ['equals',
                'contains',
                'in_list',
                'greater_than',
                'greater_or_equal_to',
                'less_than',
                'less_or_equal_to'],
                'visible_name': 'Device Name'
            },
            etc
        ]


        TODO Change `allowed_filters` based on column `type`

        """

        col_filters = []
        for col in attributes["columns"]:

            col_filter = {
                "column": col["prop"],
                "allowed_filters": all_allowed_filters,
                "visible_name": col["name"],
            }

            col_filters.append(col_filter)

        return col_filters

    def build_attributes(self, *args, **kwargs):
        """
        See `report_components.attributes` functions for more info
        """
        return component_attributes_mapper[self.component_type](*args, **kwargs)

    def build_style_attributes(self, *args, **kwargs):
        """
        See `report_components.style_attributes` dataclass for more info
        """
        return flat_dict(*args, **kwargs)

    def get_mongo_match_filters(self, flask_request):
        """
        Create a mongo `$match` filter with tenant_id and filters sent from frontend
        """

        received_filters = flask_request.json or []

        # Inserting filter by tenant_id
        received_filters.insert(
            0,
            {
                "column": "tenant_id",
                "filter_type": "equals",
                "filter_value": flask_request.headers.get("Tenantid"),
            },
        )

        filters = build_match_expression(received_filters)

        return filters

    def get_data(self, flask_request: Request):
        """
        Synopsis:

        match_filters = self.get_mongo_match_filters(flask_request)

        pipeline = [
            custom pipeline
        ]

        pipeline.insert(0, match_filters)

        results = ['mongo pipeline result'] //ex: mongodata.aggregate(pipeline, collection='Data')

        return results

        """
        raise NotImplementedError(
            "Retrival of data for this component is not implemented"
        )

    def set_attributes(self):
        raise NotImplementedError("Please overwrite method `set_attributes`")

    def set_style_attributes(self):
        raise NotImplementedError("Please overwrite method `set_style_attributes`")

    def set_allowed_filters(self):
        ...  # Component filters are optional, Report filters are needed

    def get_registration_payload(self):

        if not self.attributes:
            attributes = self.set_attributes()
            if attributes:
                self.attributes = attributes

        if not self.style_attributes:
            style_attributes = self.set_style_attributes()
            if style_attributes:
                self.style_attributes = style_attributes

        if not self.filters:
            allowed_filters = self.set_allowed_filters()
            if allowed_filters:
                self.filters = allowed_filters

        return {
            "app_id": envs.APP_ID,
            "title": self.title,
            "order": self.order,
            "component_id": self.component_id,
            "description": self.description,
            "path": self.path,
            "url": self.url,
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "style_attributes": self.style_attributes,
            "attributes": self.attributes,
            "component_type": self.component_type,
            "filters": self.filters,
        }

    def register_component(self):

        payload = self.get_registration_payload()

        response, status_code = register_component(**payload)

        if status_code not in {200, 201}:
            raise Exception("Report Component failed to register!")

        return response, status_code
