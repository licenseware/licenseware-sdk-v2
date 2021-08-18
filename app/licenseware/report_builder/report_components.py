from enum import Enum
from marshmallow import Schema, fields

from some_module import fetch_summary_data

# create a schema for each component for validation

history_overview_data = {
    "component_id": "overview",
    "url": "/overview",
    "order": 1,
    "style_attributes": {
        "width": "1/3"
    },
    "attributes": {
        "series": [
            {
                "value_description": "Devices Analyzed",
                "value_key": "devices_analyzed",
                "icon": "DeviceIcon"
            },
            {
                "value_description": "Files Analyzed",
                "value_key": "files_analyzed",
                "icon": "FileIcon"
            }
        ]
    },
    "title": "Overview",
    "type": "summary",
}

# Independent report components
# - endpoint
# - data_method
# - params inserted by user: title, width, type
# - register components to registry service : component_id, description, name, available types (ui shape in which data is shown)


report_components = ['PieChart',
 'Table',
 'Summary',
 'BarChart',
 'DetailSummary']



class flags(Enum):
    BETA = "beta"

flags.BETA

class width(Enum):
    one_third = "1/3"
    full = "full"


class components(Enum):
    summary = "summary"


class icons(Enum):
    file_icon = "FileIcon"
    device_icon = "DeviceIcon"



class SummarySeriesSchema(Schema):
    value_description = fields.String(required=True)
    value_key = fields.String(required=True)
    icon = fields.String(required=False)
    
class SummaryAttributesSchema(Schema):
    series = fields.List(fields.Nested(SummarySeriesSchema), required=True)        

class SummaryComponentSchema(Schema):
    component_id = fields.String(required=True)
    title = fields.String(required=True)
    attributes = fields.Dict(fields.Nested(SummaryAttributesSchema), required=True)
    style_attributes = fields.String(required=False, default=width.one_third)
    order = fields.Integer(required=False, allow_none=True)
    url = fields.String(required=False, allow_none=True)
    type = fields.String(required=False, default=components.summary)


class SummaryComponent:
    ...


class ReportComponents:
    
    SummaryComponent = SummaryComponent



summary_instance = ReportComponents.SummaryComponent(
    # we can generate component id from title (urls are namespaced)
    title = "Overview",  
    # will generate atributes + series
    attributes = [
        {"name": "Devices Analyzed", "icon": icons.device_icon},
        {"name": "Files Analyzed", "icon": icons.file_icon}, 
    ],
    data_method=fetch_summary_data
)

# or

summary_instance = SummaryComponent(
    title = "Overview",
    component_type="pie",
    width="constants",
    attributes = [
        {"name": "Devices Analyzed", "icon": icons.device_icon},
        {"name": "Files Analyzed", "icon": icons.file_icon}, 
    ],
    data_method=fetch_summary_data,
    # kwargs
)

history_overview_data = {
    "component_id": "overview", # independent id
    "url": "/overview",
    "order": 1,
    "style_attributes": {
        "width": "1/3"
    },
    "attributes": {
        "series": [
            {
                "value_description": "Devices Analyzed",
                "value_key": "devices_analyzed",
                "icon": "DeviceIcon"
            },
            {
                "value_description": "Files Analyzed",
                "value_key": "files_analyzed",
                "icon": "FileIcon"
            }
        ]
    },
    "title": "Overview",
    "type": "summary",
}
