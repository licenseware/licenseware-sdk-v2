from typing import Callable
from app.licenseware.common.constants import icons



class SummaryReportComponent:
    
    def __init__(
        self,
        title:str,
        component_id:str,
        fetch_function:Callable,
        icon:str, 
        path:str = None,
        order:int = None,
        style_props:list = None,
        data_props:list = None,
        component_type:str = 'summary',
    ):
        self.title = title
        self.fetch_function = fetch_function
        self.component_id = component_id
        self.path = path or '/' + component_id 
        # When path is called is here data required to fill the front-end ui component is gathered
        self.order = order
        # order - tells front-end where this component is stacked in the ui (1 place it first in the report, 2 second and so on)
        self.style_props = style_props
        # style - holds a dictionary with custom ui properties (like width size, color, height etc)
        self.data_props = data_props
        # attributes - tells front-end where in this component to place the data fetched
        self.component_type = component_type
        self.icon = icon
        
        
    def get_component_data(self, *args, **kwargs):
        # Usually data method receives a tenant_id and a custom filter
        data = self.fetch_function(*args, **kwargs)
        #TODO check first item in the list to see if data is in the proper summary report component format
        return data
        
        
   
   
    
    

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

