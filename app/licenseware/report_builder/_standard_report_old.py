"""

Register a report to registry service

from licenseware import StandardReport
or
from licenseware.standard_report import StandardReport

"""

import os
import requests
from licenseware.utils.log_config import log
from licenseware.decorators.auth_decorators import authenticated_machine


class StandardReport:

    def __init__(
        self, 
        app_id, 
        report_id, 
        report_name, 
        description, 
        url, 
        connected_apps, 
        flags=[], 
        _filter=None
    ):
        self.app_id = app_id
        self.report_id = report_id
        self.report_name = report_name
        self.description = description
        self.url = url #report_url
        self.flags=flags
        self.components = {}
        if _filter: self.register_filter(_filter)
        self.connected_apps = connected_apps        
        self.root_url = os.getenv("APP_BASE_PATH") + os.getenv("APP_URL_PREFIX")
        self.refresh_registry_url = self.root_url + '/register_all'


    def register_component_from_data(self, component_data, data_method):
        component = StandardReportComponent(component_data, data_method)
        self.components[component.component_id] = component

    def register_component(self, component):
        self.components[component.component_id] = component

    def register_filter(self, filter_component):
        self._filter = filter_component

    def return_json_payload(self):
        payload = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "report_name": self.report_name,
            "description": self.description,
            "flags": self.flags,
            "report_components": [self.components[component].return_json_payload() for component in self.components],
            "filters": self._filter.filter_columns,
            "url": self.root_url + '/reports' + self.url,
            "connected_apps": self.connected_apps
        }
        return payload

    def return_component_url(self, component_id):
        return f'{self.url}{self.components[component_id].url}'

    @authenticated_machine
    def register_report(self):
        if 'true' in os.getenv('APP_AUTHENTICATED', 'false'):
       
            payload = {
                'data': [{
                    "app_id": self.app_id,
                    "report_id": self.report_id,
                    "report_name": self.report_name,
                    "description": self.description,
                    "flags": self.flags,
                    "url": f'{os.getenv("APP_BASE_PATH")}{os.getenv("APP_URL_PREFIX")}/reports{self.url}',
                    "refresh_registry_url": self.refresh_registry_url,
                    "connected_apps": self.connected_apps
                }]
            }
            log.info(payload)
            url = f'{os.getenv("REGISTRY_SERVICE_URL")}/reports'
            headers = {"Authorization": os.getenv('AUTH_TOKEN'), 'Accept': 'application/json'}
            registration = requests.post(
                url=url, json=payload, headers=headers
            )
            if registration.status_code == 200:
                return payload
            else:
                log.warning("Could not register reports")
                return False
        else:
            log.warning('App not registered, no auth token available')
            return False


class StandardReportComponent:

    def __init__(self, data, data_method):
        self.component_id = data["component_id"]
        self.url = data["url"]
        self.order = data["order"]
        self.title = data["title"]
        self.type = data["type"]
        self.icon = data.get("icon") #only for summary
        self.style_attributes = data["style_attributes"]
        self.attributes = data["attributes"]
        self.data_method = data_method

    def return_json_payload(self):
        return {
            "component_id": self.component_id,
            "url": self.url,
            "order": self.order,
            "style_attributes": self.style_attributes,
            "attributes": self.attributes,
            "title": self.title,
            "type": self.type,
            "icon": self.icon
        }

    def return_component_data(self, *args, **kwargs):
        return self.data_method(*args, **kwargs)


class ReportFilteringComponent:

    def __init__(self, filter_columns):
        self.filter_columns = filter_columns

    def build_match_expression(self, filter_payload):
        condition_switcher = {
            "equals": self.equals_expression_builder,
            "contains": self.contains_expression_builder,
            "in_list": self.in_list_expression_builder,
            "greater_than": self.greater_than_expression_builder,
            "greater_or_equal_to": self.greater_or_equal_to_expression_builder,
            "less_than": self.less_than_expression_builder,
            "less_or_equal_to": self.less_or_equal_to_expression_builder
        }
        parsed_filter = {}
        for filter_section in filter_payload:
            parsed_filter.update(
                condition_switcher[filter_section["filter_type"]](
                    filter_section["column"], filter_section["filter_value"]
                )
            )
        return {
            '$match': parsed_filter
        }

    @staticmethod
    def in_list_expression_builder(column, filter_value):
        return {
            '$expr': {
                '$in': [f'${column}', filter_value]
            }
        }

    @staticmethod
    def equals_expression_builder(column, filter_value):
        return {
            column: filter_value
        }

    @staticmethod
    def contains_expression_builder(column, filter_value):
        return {
            column: {'$regex': filter_value}
        }

    @staticmethod
    def greater_than_expression_builder(column, filter_value):
        return {
            column: {'$gt': filter_value}
        }

    @staticmethod
    def greater_or_equal_to_expression_builder(column, filter_value):
        return {
            column: {'$gte': filter_value}
        }

    @staticmethod
    def less_than_expression_builder(column, filter_value):
        return {
            column: {'$lt': filter_value}
        }

    @staticmethod
    def less_or_equal_to_expression_builder(column, filter_value):
        return {
            column: {'$lte': filter_value}
        }
