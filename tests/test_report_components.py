import unittest
from app.licenseware.report_components import BaseReportComponent
from app.licenseware.utils.logger import log
from app.licenseware.report_components.style_attributes import style_attributes as styles
from app.licenseware.common.constants import icons

# python3 -m unittest tests/test_report_components.py


fe_filters = [
    {
        'field_name': "name", 
        'filter_type': "equals", 
        'filter_value': "the device name"
    }
]


# Simulating a flask request object
class flask_request:
    
    json = fe_filters
        
    class headers:
        
        @classmethod
        def get(cls, tenant_id):
            assert tenant_id == "Tenantid"
            return '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'
            
         


class TestReportComponents(unittest.TestCase):
    
    def test_report_component_creation(self):
        
        class VirtualOverview(BaseReportComponent):
            
            def __init__(
                self, 
                title: str, 
                component_id: str, 
                component_type: str
            ):
                self.title = title
                self.component_id = component_id
                self.component_type = component_type
                
                super().__init__(**vars(self))
                
                
            def get_data(self, flask_request):
                
                match_filters = self.get_mongo_match_filters(flask_request)
                
                # log.info(match_filters)

                return ['mongo pipeline result']
            
            
            def set_attributes(self):
                
                # Short hand based on value_key
                # See based on component type funcs from: licenseware.report_components.attributes
                value_key_and_icon = [
                    ("number_of_devices", icons.SERVERS), 
                    ("number_of_databases", icons.DATABASE_ROUNDED)
                ]
    
                # Set values straight to self.attributes
                self.attributes = self.build_attributes(value_key_and_icon)
                
                
                # Or raw dict (same results are achived using the method up)
                
                attributes = {'series': [
                    {
                        'value_description': 'Number of devices',
                        'value_key': 'number_of_devices',
                        'icon': 'ServersIcon'
                    },
                    {
                        'value_description': 'Number of databases',
                        'value_key': 'number_of_databases',
                        'icon': 'DatabaseIconRounded'
                    }
                ]}
                
                # You can also return attributes
                return attributes
                
                
            def set_style_attributes(self):
                
                # You can set a dictionary directly or return a dict like bellow
                self.style_attributes = {
                    'width': '1/3'
                }
                
                # or import `style_attributes` dataclass
                # from app.licenseware.report_components.style_attributes import style_attributes as styles
                style_attributes = self.build_style_attributes([
                    styles.WIDTH_ONE_THIRD
                    #etc
                ])
                
                return style_attributes
                
        
        virtual_overview = VirtualOverview(
            title="Overview",
            component_id="virtual_overview",
            component_type='summary'
        )
        
        
        match_filters = virtual_overview.get_mongo_match_filters(flask_request)
        
        self.assertDictEqual(match_filters, {'$match': {'name': 'the device name', 'tenant_id': '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'}})
        
        # data method
        data = virtual_overview.get_data(flask_request)
        
        self.assertEqual(data, ['mongo pipeline result'])
        
        # payload registration
        registration_payload = virtual_overview.get_registration_payload()
        
        self.assertEqual(registration_payload['component_id'], "virtual_overview")
        self.assertEqual(registration_payload['path'], '/' + "virtual_overview")
        self.assertEqual(registration_payload['style_attributes'], {'width': '1/3'})
        self.assertEqual(registration_payload['attributes']['series'], [{'value_description': 'Number of devices', 'value_key': 'number_of_devices', 'icon': 'ServersIcon'}, {'value_description': 'Number of databases', 'value_key': 'number_of_databases', 'icon': 'DatabaseIconRounded'}])
        
        # register component to registry service
        response, status_code = virtual_overview.register_component()
        self.assertEqual(status_code, 200)
        
    
        
        
        
        
'''

ODBConsolidatedReport.register_component(StandardReportComponent(
    data={
        "component_id": "odb_overview_v2",
        "url": "/overview_v2",
        "order": 1,
        "style_attributes": {
            "width": "1/3"
        },
        "attributes": odb_overview.attributes_summary(),
        "title": "Overview",
        "type": "summary",
    }, data_method=odb_overview.return_data
))



from .utils import *

collection = "ODBData"


def return_pipeline(_filter):
    pipeline = [
        {
            '$match': _filter
        }, {
            '$group': {
                '_id': None,
                'devices': {
                    '$addToSet': '$device_name'
                },
                'databases': {
                    '$addToSet': '$database_name'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'number_of_devices': {
                    '$size': '$devices'
                },
                'number_of_databases': {
                    '$size': '$databases'
                }
            }
        }
    ]
    log.warning(pipeline)
    return pipeline


def attributes_table():
    return {
        'columns': [
            {
                'name': 'Number of Devices',
                'prop': 'number_of_devices'
            },
            {
                'name': 'Number of Databases',
                'prop': 'number_of_databases'
            },

        ]
    }


def attributes_summary():
    return {
        "series": [
            {
                "value_description": "Number of Devices",
                "value_key": "number_of_devices",
                "icon": "ServersIcon"
            },
            {
                "value_description": "Number of Databases",
                "value_key": "number_of_databases",
                "icon": "DatabaseIconRounded"
            }
        ]
    }


def return_data(_request, _filter=None):
    _filter = build_tenant_filter(_request, _filter)
    data = mongodata.aggregate(return_pipeline(_filter), collection=collection)
    log.warning(data)
    return data

'''