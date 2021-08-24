from typing import Callable, List




class SummaryReportComponent:
    """
    
    Description of parameters
    
    :title - title of the ui component
    :component_id - string lowercase with underscores like `overview_id`  
    :fetch_function - the function reponsible for getting data from database
    :machine_names_icons - needs to be filled with a list of tuples like [("number_of_devices", "ServersIcon")] (machine_name and it's corespondent icon)  
    :main_icon - main icon to be used in front-end use licenseware.common.constants.icons dataclass
    :path - endpoint which when it's called will trigger fetch_function
    :order - the index where this component will be stacked/rendered in the report
    :style_props - css attributes/properties that will be applied to this component. Use report_components.style_props dataclass
    :data_props - properties which will be used in front-end show text data
    :component_type - the type of this component which coresponds in front-end to an ui component type
    
    """
    
    def __init__(
        self,
        title:str,
        component_id:str,
        fetch_function:Callable,
        main_icon:str, 
        machine_names_icons:List[tuple] = None,
        data_props:list = None,
        style_props:list = None,
        path:str = None,
        order:int = None,
        component_type:str = 'summary',
    ):
        self.title = title
        self.fetch_function = fetch_function
        self.component_id = component_id
        self.path = path or '/' + component_id 
        self.order = order
        
        self.style_props = flat_dict(style_props)
        
        if machine_names_icons is None and data_props is None:
            raise Exception("Please fill `machine_names_icons` or `data_props` parameter")
        
        self.data_props = summary_props(machine_names_icons) or flat_dict(data_props) 
        self.component_type = component_type
        self.main_icon = main_icon
        
        self.componentvars = vars(self)
        
        
    def get_component_data(self, tenant_id, filters=None):
        data = self.fetch_function(tenant_id, filters)
        return data
    
    
    def get_component_metadata(self):
        return self.componentvars
    

{'data': [{'app_id': 'ifmp', 'report_id': 'virtualization_details', 'report_name': 'Virtualization Details', 'description': 'This report gives you a detailed view of your virtual infrastructure. Deep dive into the infrastructure topology, identify devices with missing host details and capping rules for licensing.', 'flags': [], 'url': 'http://localhost:5000/ifmp/reports/virtualization_details', 'report_components': [{'title': 'Overview', 'order': 1, 'url': 'http://localhost:5000/ifmp/reports/virtualization_details/virtual_overview', 'component_id': 'virtual_overview', 'icon': 'ServersIcon', 'type': 'summary', 'style_attributes': {'width': '1/3'}, 'attributes': {'series': [{'name': 'Number of devices', 'machine_name': 'number_of_devices', 'icon': 'ServersIcon'}, {'name': 'Number of databases', 'machine_name': 'number_of_databases', 'icon': 'DatabaseIconRounded'}]}}], 'connected_apps': ['ifmp-service']}]}





"""
VirtualizationReport.register_component(StandardReportComponent(
    data={
        "component_id": "virtual_overview",
        "url": "/virtual_overview",
        "order": 1,
        "style_props": {
            "width": "1/3"
        },
        "attributes": {
            "series": [
                {
                    "value_description": "Missing parent details",
                    "value_key": "missing_parent_details",
                    "icon": "FeaturesIcon"
                },
                {
                    "value_description": "Unknown device types",
                    "value_key": "unknown_types",
                    "icon": "ServersIcon"
                },
                {
                    "value_description": "Missing cores info",
                    "value_key": "missing_cores_info",
                    "icon": "CpuIcon"
                }
            ]
        },
        "title": "Overview",
        "type": "summary",
        "icon": "ServersIcon"
    }, fetch_function=IFMPComponents.virtualization_overview
))



@staticmethod
def virtualization_overview(tenant_id, _filter=None):
    pipeline = [
        {
            '$match': {
                'tenant_id': tenant_id
            }
        }, {
            '$facet': {
                'missing_device_type': [
                    {
                        '$match': {
                            'device_type': 'Unknown'
                        }
                    }, {
                        '$group': {
                            '_id': {
                                'device_type': '$device_type'
                            },
                            'missing_device_type': {
                                '$sum': 1
                            }
                        }
                    }, {
                        '$project': {
                            '_id': 0
                        }
                    }
                ],
                'missing_parent_details': [
                    {
                        '$match': {
                            'device_type': {
                                '$ne': 'Physical'
                            },
                            'is_child_to': {
                                '$eq': None
                            }
                        }
                    }, {
                        '$group': {
                            '_id': {
                                'parent': '$is_child_to'
                            },
                            'missing_parent_details': {
                                '$sum': 1
                            }
                        }
                    }, {
                        '$project': {
                            '_id': 0
                        }
                    }
                ],
                'missing_cores_info': [
                    {
                        '$match': {
                            'total_number_of_cores': {
                                '$eq': None
                            }
                        }
                    }, {
                        '$group': {
                            '_id': {
                                'total_number_of_cores': 'total_number_of_cores'
                            },
                            'missing_cores_info': {
                                '$sum': 1
                            }
                        }
                    }, {
                        '$project': {
                            '_id': 0
                        }
                    }
                ]
            }
        }, {
            '$project': {
                'missing_cores_info': {
                    '$first': '$missing_cores_info.missing_cores_info'
                },
                'missing_device_type': {
                    '$first': '$missing_device_type.missing_device_type'
                },
                'missing_parent_details': {
                    '$first': '$missing_parent_details.missing_parent_details'
                }
            }
        }
    ]
    if _filter:
        pipeline.insert(0, _filter)
    overview, status = im(collection="IFMPData").return_aggregated(pipeline)

    if status != 200:
        return [{
            "missing_cores_info": None,
            "missing_device_type": None,
            "missing_parent_details": None,
        }], 400

    return overview, status



from flask import request
from flask_restx import Resource

from ..reports.virtualization_report import VirtualizationReport as VirtReport
from licenseware.decorators import header_doc_decorator, authorization_check

from ..dto.standard_report_dto import StandardReportDTO

api = StandardReportDTO.api
filter_model = StandardReportDTO.filter_payload
parser = header_doc_decorator(api)


@api.route(VirtReport.url)
class VirtReportController(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        return VirtReport.return_json_payload()

    @api.route(VirtReport.return_component_url("virtual_overview"))
    class VirtReportOverview(Resource):

        @api.expect(parser)
        @authorization_check
        def get(self):
            tenant_id = request.headers.get("TenantId")
            return VirtReport.components["virtual_overview"].return_component_data(tenant_id)

        @api.expect(parser)
        @api.marshal_list_with(filter_model)
        @authorization_check
        def post(self):
            tenant_id = request.headers.get("TenantId")
            filter_payload = request.json
            parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
            return VirtReport.components["virtual_overview"].return_component_data(tenant_id, _filter=parsed_filters)

@api.route(VirtReport.return_component_url("ifmp_virtual_physical"))
class VirtReportDeviceTypeOverview(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        tenant_id = request.headers.get("TenantId")
        return VirtReport.components["ifmp_virtual_physical"].return_component_data(tenant_id)

    @api.expect(parser)
    @api.marshal_list_with(filter_model)
    @authorization_check
    def post(self):
        tenant_id = request.headers.get("TenantId")
        filter_payload = request.json
        parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
        return VirtReport.components["ifmp_virtual_physical"].return_component_data(tenant_id,
                                                                                    _filter=parsed_filters)

@api.route(VirtReport.return_component_url("ifmp_devices_by_virtualization"))
class VirtReportOSOverview(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        tenant_id = request.headers.get("TenantId")
        return VirtReport.components["ifmp_devices_by_virtualization"].return_component_data(tenant_id)

    @api.expect(parser)
    @api.marshal_list_with(filter_model)
    @authorization_check
    def post(self):
        tenant_id = request.headers.get("TenantId")
        filter_payload = request.json
        parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
        return VirtReport.components["ifmp_devices_by_virtualization"].return_component_data(tenant_id, _filter=parsed_filters)

@api.route(VirtReport.return_component_url("ifmp_devices_by_os_and_type"))
class VirtReportTopologyGraph(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        tenant_id = request.headers.get("TenantId")
        return VirtReport.components["ifmp_devices_by_os_and_type"].return_component_data(tenant_id)

    @api.expect(parser)
    @api.marshal_list_with(filter_model)
    @authorization_check
    def post(self):
        tenant_id = request.headers.get("TenantId")
        filter_payload = request.json
        parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
        return VirtReport.components["ifmp_devices_by_os_and_type"].return_component_data(tenant_id,
                                                                                            _filter=parsed_filters)

@api.route(VirtReport.return_component_url("ifmp_virtual_relationships"))
class VirtReportAllDevicesTable(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        tenant_id = request.headers.get("TenantId")
        return VirtReport.components["ifmp_virtual_relationships"].return_component_data(tenant_id)

    @api.expect(parser)
    # @api.expect(filter_model, validate=True)
    @api.marshal_list_with(filter_model)
    @authorization_check
    def post(self):
        tenant_id = request.headers.get("TenantId")
        filter_payload = request.json
        parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
        return VirtReport.components["ifmp_virtual_relationships"].return_component_data(tenant_id, _filter=parsed_filters)

@api.route(VirtReport.return_component_url("ifmp_topology_graph"))
class VirtReportTopologyGraph(Resource):

    @api.expect(parser)
    @authorization_check
    def get(self):
        tenant_id = request.headers.get("TenantId")
        return VirtReport.components["ifmp_topology_graph"].return_component_data(tenant_id)

    @api.expect(parser)
    @api.marshal_list_with(filter_model)
    @authorization_check
    def post(self):
        tenant_id = request.headers.get("TenantId")
        filter_payload = request.json
        parsed_filters = VirtReport._filter.build_match_expression(filter_payload)
        return VirtReport.components["ifmp_topology_graph"].return_component_data(tenant_id, _filter=parsed_filters)

@api.route(f'{VirtReport.url}/register')
class VirtReportRegistrationEndpoint(Resource):

    @api.expect(parser)
    @authorization_check
    def post(self):
        return VirtReport.register_report()
        
        
"""

